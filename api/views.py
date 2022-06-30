from rest_framework.generics import ListAPIView
from .serializers import OrderSerializer

from orders.models import Order


class OrdersListAPIView(ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.exclude(is_deleted=True)
