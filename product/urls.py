from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

# /product/
router = DefaultRouter()
router.register('management', views.ProductView, basename='index')
router.register('category', views.CategoryView, basename="category")
router.register('images', views.ProductImageView, basename="images")

urlpatterns = [
    path('', include(router.urls)),      
]