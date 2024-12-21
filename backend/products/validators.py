from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Product


def validate_title(value):
    product = Product.objects.filter(title__iexact=value)
    if product.exists():
        raise serializers.ValidationError(f"{value} already is there.")
    return value


def validate_no_hello_in_title(value):
    if "hello" in value.lower():
        raise serializers.ValidationError("Hello not allowed in title")
    return value


unique_title_validator = UniqueValidator(
    queryset=Product.objects.all(), lookup='iexact')
