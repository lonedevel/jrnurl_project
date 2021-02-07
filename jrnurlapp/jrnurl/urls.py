from django.urls import path, include
from rest_framework.routers import DefaultRouter
from jrnurl import views

app_name = 'jrnurl'

router = DefaultRouter()
router.register('urlcollection', views.URLCollectionViewSet)
# router.register('urlcollection/<uuid:pk>', views.URLCollectionDetail)
router.register('urlitem', views.URLItemViewSet)

urlpatterns = [
    path('', include(router.urls))
]
