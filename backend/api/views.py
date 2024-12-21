from rest_framework.views import APIView
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated
# from rest_framework.permissions import isAuthenticated, isAuthenticatedOrRead
from rest_framework.decorators import api_view, permission_classes
import json
from django.forms.models import model_to_dict
from django.http import JsonResponse
from products.models import Product

from rest_framework.response import Response
from rest_framework.decorators import api_view
from products.serializers import ProductSerializer


@api_view(["POST"])
def api_home(request, *args, **kwargs):
    """
    DRF API View
    """
    # instance = Product.objects.order_by("?").first()
    # data = {}
    # if instance:
    #     data = ProductSerializer(instance).data
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # instance = serializer.save()
        data = serializer.data
        return JsonResponse(data)
    # return Response({"message": "Invalid data"}, status=400)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def index(request, *args, **kwargs):
    pass


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class Example(APIView):
    permission_classes = [IsAuthenticated | ReadOnly]
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Book.objects.all()

    def get_permissions(self):
        pass

    def get_serializer(self):
        pass

    def get(self, request, *args, **kwargs):
        pass


class BlockListPermission(BasePermission):
    def has_permission(self, request, view):
        ip_addr = request.META['REMOTE_ADDR']
        blocked = BlockList.objects.filter(ip_addr=ip_addr).exists()
        return not blocked


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, instance):
        user = request.user
        if user == instance.owner:
            return True
        return request.method in SAFE_METHODS
