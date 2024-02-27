from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

# /inventory/
router = DefaultRouter()
router.register('size', views.SizeView, basename="size")
router.register('size-varient', views.ProductSizeVarientView, basename="size-varient")

urlpatterns = [
    path('', include(router.urls)),      
]