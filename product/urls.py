from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('product', ProductModelViewSet)
router.register('category', CategoryAPIView)

urlpatterns = [
    path('', include(router.urls))
]