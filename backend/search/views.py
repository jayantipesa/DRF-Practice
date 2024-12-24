from rest_framework import generics

from products.models import Product
from products.serializers import ProductSerializer


class SearchListView(generics.ListAPIView):
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
