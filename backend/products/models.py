from django.conf import settings
from django.db import models
from django.db.models import Q

User = settings.AUTH_USER_MODEL  # auth.User

# Create your models here.


class ProductQueryset(models.QuerySet):
    def is_public(self):
        return self.filter(public=True)

    def search(self, search_str, user=None):
        lookup = Q(title__icontains=search_str) | Q(
            content__icontains=search_str)

        qs = self.is_public().filter(lookup)
        if user is not None:
            user_specific_qs = self.filter(user=user).filter(lookup)
            qs = (qs | user_specific_qs).distinct()
        return qs

        # inorder to do lookup via dict object
        # dict_lookup = {
        #     'title__icontains': search_str,
        #     'content__icontains': search_str
        # }
        # self.filter(**dict_lookup)


class ProductManager(models.Manager):
    # The Queryset class is connected to Manager class via get_queryset method
    def get_queryset(self, *args, **kwargs):
        return ProductQueryset(self.model, using=self._db)

    # It is a good coding practice to always call the methods of queryset in
    # the manager instead of computing qs by itself.
    def search(self, query, user=None):
        return self.get_queryset().search(query, user=user)


class Product(models.Model):
    user = models.ForeignKey(User, default=1, null=True,
                             on_delete=models.SET_NULL
                             )
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=99.99)
    public = models.BooleanField(default=True)

    objects = ProductManager()

    @property
    def sale_price(self):
        return f"{float(self.price) * 0.8: .2f}"

    def get_discount(self):
        return "122"
