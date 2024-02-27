from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

# /order/
router = DefaultRouter()
router.register('cod', views.CodOrderView, basename='cod')

urlpatterns = [
    path('', include(router.urls)),      
]