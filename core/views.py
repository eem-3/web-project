from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.http import HttpResponse
from .forms import BootstrapUserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Entity, Project, Media, Comment, Tag, Status
from rest_framework import generics
from .serializers import EntitiesSerializer, MediaSerializer, ProjectSerializer, StatusSerializer, TagSerializer

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




### API ###
class APIEntityList(generics.ListCreateAPIView):
    queryset = Entity.objects.all()
    serializer_class = EntitiesSerializer

class APIEntityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Entity.objects.all()
    serializer_class = EntitiesSerializer

class APIMediaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer

class APIProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class APIStatusList(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class APIStatusDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class APITagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class APITagDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer