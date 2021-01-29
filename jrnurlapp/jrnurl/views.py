# from rest_framework.decorators import action
# from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import URLCollection, URLItem
from . import serializers


class URLCollectionViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           mixins.DestroyModelMixin):
    """Manage URLCollections in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = URLCollection.objects.all()
    serializer_class = serializers.URLCollectionSerializer

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class URLItemViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin,
                     mixins.DestroyModelMixin):
    """Manage URLItems in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = URLItem.objects.all()
    serializer_class = serializers.URLItemSerializer

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)
