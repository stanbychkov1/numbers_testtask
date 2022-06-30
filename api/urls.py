from django.urls import path

from .views import OrdersListAPIView


urlpatterns = [
    path('orders/', OrdersListAPIView.as_view()),
]
