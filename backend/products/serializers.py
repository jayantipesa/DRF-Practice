from rest_framework import serializers
from rest_framework.reverse import reverse
from django.db.models import Q

from api.serializers import UserSerializer
from .models import Product
from . import validators


class UserProductSerializer(serializers.Serializer):
    title = serializers.CharField(read_only=True)
    product_url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='pk',
        read_only=True
    )


class ProductSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    related_products = serializers.SerializerMethodField(read_only=True)
    # email = serializers.EmailField(source='user.email', read_only=True)
    my_discount = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='pk'
    )
    # edit_url = serializers.HyperlinkedIdentityField(
    #     view_name='product-edit',
    #     lookup_field='pk'
    # )

    title = serializers.CharField(validators=[
        # validators.validate_title,
        validators.validate_no_hello_in_title,
        validators.unique_title_validator
    ])
    name = serializers.CharField(source='title', read_only=True)
    # email = serializers.EmailField(write_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'user',
            'related_products',
            'title',
            'name',
            'content',
            'price',
            'sale_price',
            'my_discount',
            'edit_url',
            'url',
            # 'email'
        ]

    """
        You can also define validators externally in validators.py file or in models.py itself
        The advantage of doing it here is you get access to the request object in the context
        and you can use additional properties of it like user, client etc
    """
    # def validate_title(self, value):
    #     product = Product.objects.filter(title__iexact=value)
    #     if product.exists():
    #         raise serializers.ValidationError(
    #             f"{value} is already a defined product.")
    #     return value

    def create(self, validated_data):
        # request = self.context.get('request')
        # validated_data['user'] = request.user
        # email = validated_data.pop('email', None) or 'jayanti.pesa@gmail.com'
        # Product.objects.create(**validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # email = validated_data.pop('email', None) or 'jayanti.pesa@gmail.com'
        return super().update(instance, validated_data)

    def get_edit_url(self, obj):
        request = self.context.get('request', None)
        if request is None:
            return None
        return reverse('product-edit', kwargs={'pk': obj.pk}, request=request)

    def get_my_discount(self, obj):
        if not hasattr(obj, 'id'):
            return None
        if not isinstance(obj, Product):
            return None
        return obj.get_discount()

    def get_related_products(self, obj):
        # fetching all products except the current product instance
        related_products_qs = obj.user.product_set.filter(~Q(id=obj.id))
        return UserProductSerializer(
            related_products_qs,
            many=True,
            context=self.context
        ).data
