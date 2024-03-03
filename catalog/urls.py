from django.urls import path

from .views import index, show_category, show_product

urlpatterns = [
    path('', index, {'template_name': 'catalog/index.html'}, name='catalog_home'),
    path('category/<slug:category_slug>/', show_category, {'template_name': 'catalog/category.html'}, name='catalog_category'),
    path('product/<slug:product_slug>/', show_product, {'template_name': 'catalog/product.html'}, name='catalog_product'),
]
