from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import BootstrapUserCreationForm
from .models import Entity, Project, Media, Comment


def view_home(request):
    if request.user.is_authenticated:
        entities = Entity.objects.all()
        return render(request, 'components/home.html', {'entities': entities})
    return render(request, 'components/homedemo.html')


class SignUpView(CreateView):
    """Sign up view."""
    form_class = BootstrapUserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')


def entity_detail(request, pk):
    entity = get_object_or_404(Entity, pk=pk)
    project = getattr(entity, 'project', None)
    media = getattr(entity, 'media', None)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        text = request.POST.get('comment_text', '').strip()
        parent_id = request.POST.get('parent_id', '').strip()
        if text:
            parent = None
            if parent_id:
                parent = Comment.objects.filter(comment_id=parent_id, entity=entity).first()
            Comment.objects.create(entity=entity, user=request.user, text=text, parent=parent)
        return redirect(request.path + '#comments')

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
