from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import URLCollection, URLItem
from . import serializers


class URLCollectionViewSet(viewsets.ModelViewSet):
    """Manage URLCollections in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = URLCollection.objects.all()
    serializer_class = serializers.URLCollectionSerializer

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class URLItemViewSet(viewsets.ModelViewSet):
    """Manage URLItems in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = URLItem.objects.all()
    serializer_class = serializers.URLItemSerializer

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)
