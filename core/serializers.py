from rest_framework import serializers
from core.models import Entity, Tag, Media, Project, Comment, Report, Status


class StatusSerializer(serializers.HyperlinkedModelSerializer):
    uri = serializers.HyperlinkedIdentityField(view_name='status-detail')

    class Meta:
        model = Status
        fields = ('uri', 'status_id', 'status')


class TagSerializer(serializers.HyperlinkedModelSerializer):
    uri = serializers.HyperlinkedIdentityField(view_name='tag-detail')

    class Meta:
        model = Tag
        fields = ('uri', 'tag_id', 'tag')


class EntitiesSerializer(serializers.HyperlinkedModelSerializer):
    uri = serializers.HyperlinkedIdentityField(view_name='entity-detail')
    user = serializers.CharField(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    status = StatusSerializer(read_only=True)

    class Meta:
        model = Entity
        fields = (
            'uri', 'entity_id', 'title', 'description', 'description_ai',
            'user', 'type', 'up_votes', 'status', 'created_at', 'tags'
        )



class MediaSerializer(serializers.HyperlinkedModelSerializer):
    uri = serializers.HyperlinkedIdentityField(view_name='media-detail')
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Media
        fields = (
            'uri', 'entity_id', 'title', 'description', 'user', 'file',
            'storage_url', 'filename', 'mimetype', 'size', 'up_votes'
        )


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    uri = serializers.HyperlinkedIdentityField(view_name='project-detail')
    user = serializers.CharField(read_only=True)

    media_items = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='media-detail'
    )

    class Meta:
        model = Project
        fields = (
            'uri', 'entity_id', 'title', 'description', 'user',
            'media_items', 'up_votes', 'created_at'
        )


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    uri = serializers.HyperlinkedIdentityField(view_name='comment-detail')
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Comment
        fields = ('uri', 'comment_id', 'entity', 'user', 'parent', 'text', 'created_at')