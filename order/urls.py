from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

# /order/
router = DefaultRouter()
router.register('cod', views.CodOrderView, basename='cod')
router.register('custom', views.CustomOrderView, basename='custom')

urlpatterns = [
    path('', include(router.urls)),      
]