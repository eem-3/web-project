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
    entity_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    description_ai = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.SmallIntegerField()
    up_votes = models.IntegerField(default=0)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(
        Tag,
        related_name='entities',
        blank=True,
    )
    votes = models.ManyToManyField(
        User,
        related_name='upvoted_entities',
        blank=True
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.type == 1:
            return reverse('core:project_detail', kwargs={'pk': self.pk})
        elif self.type == 2:
            return reverse('core:media_detail', kwargs={'pk': self.pk})
        return reverse('core:home')


class Media(Entity):
    file = models.FileField(upload_to='uploads/%Y/%m/%d', null=True)
    # Cambia esta línea:
    storage_url = models.TextField(blank=True, null=True)
    filename = models.CharField(max_length=255, blank=True)
    mimetype = models.CharField(max_length=100, blank=True)
    size = models.BigIntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.file:
            if not self.size:
                self.size = self.file.size
            if not self.filename:
                self.filename = self.file.name
            # Si no tienes una URL externa, puedes guardar la ruta del archivo por defecto
            if not self.storage_url:
                self.storage_url = self.file.url

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:media_detail', kwargs={'pk': self.pk})

class Project(Entity):
    media_items = models.ManyToManyField(
        Media,
        related_name='projects',
        blank=True,
    )

    def get_absolute_url(self):
        return reverse('core:project_detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
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
