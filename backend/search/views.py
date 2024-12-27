from rest_framework import generics
from rest_framework.response import Response
from products.models import Product
from products.serializers import ProductSerializer
from . import client


class SearchListView(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        search_term = request.GET.get('q', None)
        tag = request.GET.get('tag') or None
        user = None
        if request.user.is_authenticated:
            user = request.user.username
        results = Product.objects.none()
        if search_term is not None:
            results = client.perform_search(search_term, tags=tag, user=user)
        return Response(results)


class SearchListOldView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        search_term = self.request.GET.get('q', None)
        results = Product.objects.none()
        if search_term is not None:
            user = None
            if self.request.user.is_authenticated:
                user = self.request.user
            results = qs.search(search_term, user=user)
        return results
