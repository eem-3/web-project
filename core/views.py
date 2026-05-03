import uuid

from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import HttpResponse
from .forms import BootstrapUserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Entity, Project, Media, Comment, Tag

def view_home(request):
    if request.user.is_authenticated:
        llista_entitats = Entity.objects.all()
        return render(request, 'components/home.html', {'entities': llista_entitats})
    else:
        return render(request, 'components/homedemo.html')

class SignUpView(CreateView):
    """Sign up view."""
    form_class = BootstrapUserCreationForm         # the form to show (username + password + confirm)
    template_name = 'registration/signup.html'     # the HTML template to render
    success_url = reverse_lazy('login')            # after signup, redirect to the login page


def EntityView1(request, pk):
    # Obtenemos la entidad base
    entity = get_object_or_404(Entity, pk=pk)

    # Intentamos obtener la versión específica (Project o Media)
    # Django permite acceder al "hijo" desde el "padre" en minúsculas
    project = getattr(entity, 'project', None)
    media = getattr(entity, 'media', None)

    # Obtenemos los comentarios asociados a esta entidad
    comments = Comment.objects.filter(entity=entity).order_by('-created_at')

    context = {
        'entity': entity,
        'project': project,
        'media': media,
        'comments': comments,
    }

    return render(request, 'components/entity_detail.html', context)


class PostCreateProject(CreateView):
    model = Project
    fields = ['title', 'description', 'status', 'tags', 'media_items']
    template_name = 'components/project_form.html'
    success_url = reverse_lazy('core:home')

    def post(self, request, *args, **kwargs):
        data = request.POST.copy()
        tags_enviats = data.getlist('tags')

        nous_ids = []
        for valor in tags_enviats:
            valor = valor.strip()
            if not valor:
                continue

            es_uuid = False
            try:
                uuid.UUID(valor)
                es_uuid = True
            except ValueError:
                es_uuid = False

            if es_uuid:
                tag_existent = Tag.objects.filter(tag_id=valor).first()
                if tag_existent:
                    nous_ids.append(str(tag_existent.pk))
                    continue

            tag_obj, _ = Tag.objects.get_or_create(tag=valor)
            nous_ids.append(str(tag_obj.pk))

        data.setlist('tags', nous_ids)
        request.POST = data

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.type = 1
        return super().form_valid(form)

