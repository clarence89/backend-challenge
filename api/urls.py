from django.urls import path
from . import views

urlpatterns = [
    # Categories
    path("categories", views.categories),
    path("categories/<int:id>", views.category),
    path("categories/create", views.create_category),
    path("categories/<int:id>/update", views.update_category),
    path("categories/<int:id>/delete", views.delete_category),
    # Products
    path("products", views.products),
    path("products/<int:id>", views.product),
    path("products-with-category", views.products_with_category),
    path("products/<int:id>/delete", views.delete_product),
    path("products/<int:id>/update", views.update_product),
    path("products/create", views.create_product),
    path("products/<int:id>/convert", views.convert_price),
    # Derived Summary
    path("summary/total-products", views.total_products),
    path("summary/products-per-category", views.products_per_category),
]
