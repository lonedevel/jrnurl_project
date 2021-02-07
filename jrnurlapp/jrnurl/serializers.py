from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer
from core.models import URLCollection, URLItem, URLCollectionItems


class URLItemSerializer(serializers.ModelSerializer):
    """Serializer for URLItem objects"""

    class Meta:
        model = URLItem
        fields = ('id', 'title', 'url', 'visits', 'created', 'modified',
                  'tags', 'user',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        """Create new urlitem if it does not yet exist"""
        urlitem, created = URLItem.objects.get_or_create(**validated_data)
        if created:
            urlitem.save()
        return urlitem


class URLCollectionItemSerializer(serializers.ModelSerializer):
    """Serializer for the URLCollectionItem many-to-many objects"""
    class Meta:
        model = URLCollectionItems
        fields = ('collection', 'item')


class URLCollectionSerializer(WritableNestedModelSerializer,
                              serializers.ModelSerializer):
    """Serializer for URLCollection objects"""
    items = URLItemSerializer(many=True, required=False)
    # items = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     queryset=URLItem.objects.all()
    # )

    class Meta:
        model = URLCollection
        fields = ('id', 'name', 'description', 'created', 'modified',
                  'collection_type', 'tags', 'items', 'user')
        extra_kwargs = {'items': {'required': False}}

    def create(self, validated_data):
        """Create a new urlcollection if it does not exist
            and new urlitem tree if defined"""

        items = []
        if 'items' in validated_data:
            items = validated_data.pop('items')

        urlcollection, created = \
            URLCollection.objects.get_or_create(**validated_data)

        for item in items:
            item_obj = URLItem.objects.create(title=item['title'],
                                              url=item['url'],
                                              visits=item['visits'],
                                              user=item['user'])
            urlcollection.items.add(item_obj,
                                    through_defaults={'user': item['user']})

        if created:
            urlcollection.save()

        return urlcollection
