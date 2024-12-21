
from rest_framework import viewsets, mixins

from .serializers import ProductSerializer
from .models import Product
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import status


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductGenericViewSet(
    # mixins.ListModelMixin,
    # mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def list(self, request):
        products = self.get_queryset()
        data = self.get_serializer(products, many=True)
        return Response(data.data)

    def retrieve(self, request, pk=None):
        product = self.get_object()
        serializer = self.get_serializer(product)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'])
    def info(self, request, pk=None):
        product = self.get_object()
        data = {
            'product': self.get_serializer(product).data,
            'extra_info': 'test'
        }
        return Response(data)

    @action(detail=False, methods=['GET'])
    def sorted_products(self, request, *args, **kwargs):
        products = Product.objects.all().order_by('-price')
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(
            product, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# product_list_view = ProductGenericViewSet.as_view({'get': 'list'})
# product_detail_view = ProductGenericViewSet.as_view({'get': 'retrieve'})
