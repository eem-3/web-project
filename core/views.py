import uuid
import requests
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Entity, Project, Media, Comment, Tag, Status
from .forms import BootstrapUserCreationForm
from .serializers import TagSerializer


def get_api_tag_choices(request):
    """
    Obtiene los tags desde la API para popular el formulario.
    Si el DEBUG TAG aparece, confirmamos que la API responde.
    """
    try:
        api_url = request.build_absolute_uri(reverse_lazy('core:api_tags_list'))
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            return [(t['tag_id'], t['tag']) for t in response.json()]
    except Exception as e:
        print(f"Error obteniendo tags de la API: {e}")
    return []

def resolve_tag_ids(request, tags_enviats):
    """
    GESTIÓN ÚNICA:
    - Ignora el tag de debug (debug-static-id).
    - Mantiene UUIDs existentes.
    - Crea nuevos tags vía POST a la API si recibe texto plano.
    """
    nous_ids = []
    try:
        api_url = request.build_absolute_uri(reverse_lazy('core:api_tags_list'))
    except:
        api_url = request.build_absolute_uri('/api/tags/')

    for valor in tags_enviats:
        valor = valor.strip()
        # Filtro de seguridad para el tag de debug y vacíos
        if not valor or valor == 'debug-static-id':
            continue

        try:
            uuid.UUID(valor)
            nous_ids.append(valor)
        except ValueError:
            # Si no es UUID, es texto nuevo: delegamos a la API
            try:
                response = requests.post(api_url, data={'tag': valor}, timeout=5)
                if response.status_code in [200, 201]:
                    nous_ids.append(response.json().get('tag_id'))
            except Exception as e:
                print(f"Error en resolve_tag_ids via API: {e}")
    return nous_ids


def view_home(request):
    if not request.user.is_authenticated:
        return render(request, 'components/homedemo.html')

    query = request.GET.get('q', '').strip()

    entities = Entity.objects.all().prefetch_related('tags').order_by('-created_at')

    if query:
        entities = entities.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__tag__icontains=query)
        ).distinct()

    context = {
        'entities': entities,
        'query': query,
    }
    return render(request, 'components/home.html', context)

class SignUpView(CreateView):
    """Sign up view."""
    form_class = BootstrapUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


def EntityView1(request, pk):
    entity = get_object_or_404(Entity, pk=pk)
    project = getattr(entity, 'project', None)
    media = getattr(entity, 'media', None)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/accounts/login/')
        text = request.POST.get('comment_text', '').strip()
        parent_id = request.POST.get('parent_id', '').strip()
        if text:
            parent = None
            if parent_id:
                parent = Comment.objects.filter(comment_id=parent_id, entity=entity).first()
            Comment.objects.create(entity=entity, user=request.user, text=text, parent=parent)
        return HttpResponseRedirect(request.path + '#comments')

    comments = (
        Comment.objects
        .filter(entity=entity, parent=None)
        .order_by('created_at')
        .select_related('user')
        .prefetch_related('replies__user')
    )

    return render(request, 'components/entity_detail.html', {
        'entity': entity,
        'project': project,
        'media': media,
        'comments': comments,
    })


class PostCreateProject(CreateView):
    model = Project
    fields = ['title', 'description', 'tags']
    template_name = 'components/project_form.html'
    success_url = reverse_lazy('core:home')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        choices = get_api_tag_choices(self.request)
        form.fields['tags'].choices = choices
        return form

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        tags_enviats = data.getlist('tags')
        
        nous_ids = resolve_tag_ids(request, tags_enviats)
        
        data.setlist('tags', nous_ids)
        request.POST = data
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.type = 1
        try:
            form.instance.status = Status.objects.get(status_id=1)
        except Status.DoesNotExist:
            form.instance.status = Status.objects.first()
        self.object = form.save()

        files = self.request.FILES.getlist('upload_files')
        for f in files:
            new_media = Media.objects.create(
                title=f"{f.name} [{self.object.title}]",
                description=f"Resource uploaded for {self.object.title}",
                description_ai="",
                user=self.request.user,
                type=2,  # Tipus Media
                status=self.object.status,
                file=f,
                filename=f.name,
                size=f.size,
                mimetype=f.content_type,
                storage_url=""
            )
            self.object.media_items.add(new_media)

        return HttpResponseRedirect(self.get_success_url())


class MyEntitiesView(ListView):
    model = Entity
    template_name = 'components/my_entities.html'
    context_object_name = 'entities'

    def get_queryset(self):
        return Entity.objects.filter(user=self.request.user).order_by('-created_at')


class PostUpdateProject(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    fields = ['title', 'description', 'tags']
    template_name = 'components/project_form.html'
    success_url = reverse_lazy('core:my_entities')

    def test_func(self):
        try:
            project = self.get_object()
            return self.request.user == project.user
        except:
            return False

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Project.DoesNotExist:
            raise Http404("This resource is a File, not a Project, and cannot be edited this way.")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        choices = get_api_tag_choices(self.request)
        form.fields['tags'].choices = choices
        return form

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        data = request.POST.copy()
        tags_enviats = data.getlist('tags')
        
        nous_ids = resolve_tag_ids(request, tags_enviats)

        data.setlist('tags', nous_ids)
        request.POST = data
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()

        media_to_delete = self.request.POST.getlist('delete_media')
        if media_to_delete:
            self.object.media_items.remove(*media_to_delete)

        files = self.request.FILES.getlist('upload_files')
        for f in files:
            new_media = Media.objects.create(
                title=f"{f.name} (Added)",
                user=self.request.user,
                type=2,
                status=self.object.status,
                file=f,
                filename=f.name,
                mimetype=f.content_type
            )
            self.object.media_items.add(new_media)

        return HttpResponseRedirect(self.get_success_url())
    
class PostDeleteProject(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('core:my_entities')

    def test_func(self):
        return self.request.user == self.get_object().user
    

# API
# --- API VIEWS (DJANGO REST FRAMEWORK) ---

@api_view(['GET', 'POST'])
def api_tags_list(request):
    """
    Single source of truth para Tags.
    """
    if request.method == 'GET':
        tags = Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        
        # Añadimos el tag de debug manualmente a la lista serializada
        data = list(serializer.data)
        data.append({
            'tag_id': 'debug-static-id', 
            'tag': 'DEBUG TAG (API ONLY)'
        })
        return Response(data)

    if request.method == 'POST':
        tag_name = request.data.get('tag', '').strip()
        if not tag_name:
            return Response({"error": "No tag name provided"}, status=400)
        
        # Aquí la API decide si crea o recupera de la DB
        tag_obj, created = Tag.objects.get_or_create(tag=tag_name)
        serializer = TagSerializer(tag_obj)
        status_code = 201 if created else 200
        return Response(serializer.data, status=status_code)

def lista_tags_frontend(request):
    """Vista para visualizar los tags consumiendo la propia API"""
    try:
        api_url = request.build_absolute_uri(reverse_lazy('core:api_tags_list'))
        response = requests.get(api_url)
        tags_list = response.json()
    except Exception:
        tags_list = []
    return render(request, 'tags_display.html', {'tags': tags_list})