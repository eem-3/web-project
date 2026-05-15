from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
import uuid

class Status(models.Model):
    status_id = models.SmallIntegerField(primary_key=True)
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.status

class Tag(models.Model):
    tag_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tag = models.CharField(max_length=100)

    def __str__(self):
        return self.tag

class Entity(models.Model):
    MEDIA_TYPE = 1
    PROJECT_TYPE = 2
    TYPE_CHOICES = [(MEDIA_TYPE, 'Media'), (PROJECT_TYPE, 'Project')]

    entity_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    description_ai = models.TextField(blank=True, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.SmallIntegerField(choices=TYPE_CHOICES)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='entities', blank=True)
    votes = models.ManyToManyField(User, related_name='upvoted_entities', blank=True)

    def __str__(self):
        return self.title

class Media(Entity):
    file = models.FileField(upload_to='uploads/%Y/%m/%d', null=True, blank=True)
    storage_url = models.TextField(blank=True, default='')
    filename = models.CharField(max_length=255, blank=True, default='')
    mimetype = models.CharField(max_length=100, blank=True, default='')
    size = models.BigIntegerField(default=0)

    def get_absolute_url(self):
        return reverse('core:media_detail', kwargs={'pk': self.pk})

class Project(Entity):
    media_items = models.ManyToManyField(Media, related_name='projects', blank=True)

    def get_absolute_url(self):
        return reverse('core:project_detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"comment from {self.user.username} to {self.entity.entity_id} - {self.entity.title}"

class Report(models.Model):
    report_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"report from {self.user.username} to {self.entity.entity_id} - {self.entity.title}"
