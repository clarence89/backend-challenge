from django.urls import path
from . import views

urlpatterns=[
path("products",views.products),
path("products/<int:id>",views.product),
path("products-with-category",views.products_with_category),
path("products/<int:id>/convert",views.convert_price),
path("summary/total-products",views.total_products),
path("summary/products-per-category",views.products_per_category),
]