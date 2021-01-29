from rest_framework import serializers
from core.models import URLCollection, URLItem, URLCollectionItems


class URLItemSerializer(serializers.ModelSerializer):
    """Serializer for URLItem objects"""

    class Meta:
        model = URLItem
        fields = ('id', 'title', 'url', 'visits', 'created', 'modified',
                  'tags', 'user',)
        read_only_fields = ('id',)


class URLCollectionItemSerializer(serializers.ModelSerializer):
    """Serializer for the URLCollectionItem many-to-many objects"""
    class Meta:
        model = URLCollectionItems
        fields = ('collection', 'item')


class URLCollectionSerializer(serializers.ModelSerializer):
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
        items = []
        if 'items' in validated_data:
            items = validated_data.pop('items')

        urlcollection = URLCollection.objects.create(**validated_data)

        for item in items:
            item_obj = URLItem.objects.create(title=item['title'],
                                              url=item['url'],
                                              visits=item['visits'],
                                              user=item['user'])
            urlcollection.items.add(item_obj,
                                    through_defaults={'user': item['user']})

        urlcollection.save()

        return urlcollection
