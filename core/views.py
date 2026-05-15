import uuid
import requests
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import BootstrapUserCreationForm
from .models import Entity, Project, Media, Comment, Tag, Status
from .serializers import TagSerializer


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

    return render(request, 'components/home.html', {'entities': entities, 'query': query})


class SignUpView(CreateView):
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

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        nous_ids = []
        for valor in data.getlist('tags'):
            valor = valor.strip()
            if not valor:
                continue
            try:
                uuid.UUID(valor)
                if Tag.objects.filter(tag_id=valor).exists():
                    nous_ids.append(valor)
                    continue
            except ValueError:
                pass
            tag_obj, _ = Tag.objects.get_or_create(tag=valor)
            nous_ids.append(str(tag_obj.pk))
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

        for f in self.request.FILES.getlist('upload_files'):
            new_media = Media.objects.create(
                title=f"{f.name} [{self.object.title}]",
                description=f"Resource uploaded for {self.object.title}",
                description_ai='',
                user=self.request.user,
                type=2,
                status=self.object.status,
                file=f,
                filename=f.name,
                size=f.size,
                mimetype=f.content_type,
                storage_url='',
            )
            self.object.media_items.add(new_media)

        return HttpResponseRedirect(self.get_success_url())


class MyEntitiesView(LoginRequiredMixin, ListView):
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
            return self.request.user == self.get_object().user
        except Exception:
            return False

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Project.DoesNotExist:
            raise Http404("This resource is a File, not a Project, and cannot be edited this way.")

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        nous_ids = []
        for valor in data.getlist('tags'):
            valor = valor.strip()
            if not valor:
                continue
            try:
                uuid.UUID(valor)
                tag_obj = Tag.objects.filter(tag_id=valor).first()
                if tag_obj:
                    nous_ids.append(str(tag_obj.pk))
                    continue
            except ValueError:
                pass
            tag_obj, _ = Tag.objects.get_or_create(tag=valor)
            nous_ids.append(str(tag_obj.pk))
        data.setlist('tags', nous_ids)
        request.POST = data
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()

        media_to_delete = self.request.POST.getlist('delete_media')
        if media_to_delete:
            self.object.media_items.remove(*media_to_delete)

        for f in self.request.FILES.getlist('upload_files'):
            new_media = Media.objects.create(
                title=f"{f.name} (Added)",
                user=self.request.user,
                type=2,
                status=self.object.status,
                file=f,
                filename=f.name,
                mimetype=f.content_type,
            )
            self.object.media_items.add(new_media)

        return HttpResponseRedirect(self.get_success_url())


class PostDeleteProject(LoginRequiredMixin, UserPassesTestMixin, View):
    def post(self, request, pk):
        entity = get_object_or_404(Entity, pk=pk)
        if entity.user == request.user:
            entity.delete()
        return redirect('core:my_entities')

    def test_func(self):
        entity = get_object_or_404(Entity, pk=self.kwargs.get('pk'))
        return entity.user == self.request.user


# --- API views ---

@api_view(['GET', 'POST'])
def api_tags_list(request):
    if request.method == 'GET':
        tags = Tag.objects.all()
        return Response(TagSerializer(tags, many=True).data)

    if request.method == 'POST':
        tag_name = request.data.get('tag', '').strip()
        if not tag_name:
            return Response({'error': 'No tag name provided'}, status=400)
        tag_obj, created = Tag.objects.get_or_create(tag=tag_name)
        return Response(TagSerializer(tag_obj).data, status=201 if created else 200)


def lista_tags_frontend(request):
    try:
        api_url = request.build_absolute_uri(reverse_lazy('core:api_tags_list'))
        tags_list = requests.get(api_url).json()
    except Exception:
        tags_list = []
    return render(request, 'tags_display.html', {'tags': tags_list})
