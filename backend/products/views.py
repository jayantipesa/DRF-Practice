from rest_framework import authentication, generics, mixins, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import Http404
from django.shortcuts import get_object_or_404

from api.authentication import TokenAuthentication

from api.mixins import StaffEditorPermissionMixin, UserQuerySetMixin
from .models import Product
from api.permissions import IsStaffEditorPermission
from .serializers import ProductSerializer


class ProductListCreateAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.ListCreateAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    """
        Lets say we define the lookup_field here, this field is also defined and utilized in the UserQuerySetMixin mixin 
        in the get_queryset method.
        the get_queryset method is not defined in this class, so the one defined in UserQuerySetMixin will be invoked.
        when that is invoked, it will not use it's own defined lookup_field's value. It might seem like that 
        because it does self.lookup_field. 
        But the self there represents the instance of this class from which get_queryset method was called. and not
        it's own class. hence the value which will be used is the one that is defined in this class
        if not found here, then it will do the mro process again to determine from where to pick the value.
        
    """
    # lookup_field = 'user'

    """
        no longer needed as these are default authentication
        and have been defined in settings.py already
    """
    # authentication_classes = [
    #     authentication.SessionAuthentication,
    #     TokenAuthentication
    # ]

    """
        no longer needed to define them explicitily as you have inherited
        the permissionMixin which defines the permission_classes
    """
    # permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]

    """
        Ideally the data validation and transformation part should not in the view, it's better
        to keep this logic in serializer's create method
    """

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None

        if content is None:
            content = title
        serializer.save(user=self.request.user, content=content)

    """
        This is not required anymore because we have defined a generic Mixin to fetch user specific
        queryset that can be reused for other views as well.
    """
    # def get_queryset(self, *args, **kwargs):
    #     qs = super().get_queryset(*args, **kwargs)
    #     user = self.request.user
    #     if not user.is_authenticated:
    #         return Product.objects.none()
    #     return qs.filter(user=user)


class ProductDetailAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.RetrieveAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductUpdateAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.UpdateAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title


class ProductDeleteAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.DestroyAPIView
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)


# class ProductListAPIView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


class ProductMixinView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
    StaffEditorPermissionMixin
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(content=content)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def perform_update(self, serializer):
        # instance = serializer.save()
        # instance.price = 599
        # instance.content = 'Changed price via UpdateModelMixin.'
        # instance.save()
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = 'Changed price via UpdateModelMixin.'
            price = 699
            serializer.save(content=content, price=price)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method
    if method == "GET":
        if pk is not None:
            # detail view
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj, many=False).data
            return Response(data)
        # list view
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True).data
        return Response(data)

    if method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content', None)
            if content is None:
                content = title
            serializer.save(content=content)
            return Response(serializer.data)


# def sl_endpoint(
#     function=None,
#     allowed_methods=None,
#     atomic=True
# ):
#     def decorator(view_function, request, *args, **kwargs):
#         if request.method not in allowed_methods:
#             return HTTPResponseForbidden('method not allowed')
#         return view_function

#     return decorator
