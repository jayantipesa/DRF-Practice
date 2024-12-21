from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    # other_products = serializers.SerializerMethodField(read_only=True)

    # def get_other_products(self, user_obj):
    #     all_products_qs = user_obj.product_set.all()[:5]

    #     return UserProductSerializer(all_products_qs, many=True, context=self.context).data
