from django.urls import path
from . import views


urlpatterns = [
    # path('', views.ProductMixinView.as_view(), name='product_create'),
    # path('<int:pk>/', views.ProductMixinView.as_view(), name='product_detail'),

    path('', views.ProductListCreateAPIView.as_view(), name='product-create'),
    path('<int:pk>/update/', views.ProductUpdateAPIView.as_view(),
         name='product-edit'),
    path('<int:pk>/delete/', views.ProductDeleteAPIView.as_view(),
         name='product-delete'),
    path('<int:pk>/', views.ProductDetailAPIView.as_view(), name='product-detail')

    # path('', views.product_alt_view, name='product_create'),
    # path('<int:pk>/', views.product_alt_view, name='product_detail')
]
