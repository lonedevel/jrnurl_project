from rest_framework import serializers
from core.models import URLCollection, URLItem


class URLCollectionSerializer(serializers.ModelSerializer):
    """Serializer for URLCollection objects"""

    items = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=URLItem.objects.all()
    )

    class Meta:
        model = URLCollection
        fields = ('id', 'name', 'description', 'created', 'modified',
                  'collection_type', 'favorite', 'user', 'tags', 'items')
        read_only_fields = ('id',)


class URLItemSerializer(serializers.ModelSerializer):
    """Serializer for URLItem objects"""

    class Meta:
        model = URLItem
        fields = ('id', 'title', 'url', 'visits', 'created', 'modified',
                  'user',)
        read_only_fields = ('id',)
