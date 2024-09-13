from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'countries', CountryViewSet)
router.register(r'manufacturers', ManufacturerViewSet)
router.register(r'cars', CarViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', index, name='index'),
    path('export/', export_data, name='export_data'),
    path('', include(router.urls)),
]