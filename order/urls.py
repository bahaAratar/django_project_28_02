from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderModelViewSet, OrderConfirmAPIView

router = DefaultRouter()
router.register('order', OrderModelViewSet)

urlpatterns = [
    path('confirm/<uuid:code>/',OrderConfirmAPIView.as_view()),
    path('', include(router.urls)),
]