from django.urls import path
from .views import register, registration_success, products, buy_product, buy_success, write_review

urlpatterns = [
    path('register/', register, name='register'),
    path('registration_success/', registration_success, name='registration_success'),
    path('products/', products, name='products'),
    path('buy/<int:product_id>/', buy_product, name='buy_product'),
    path('buy/success/', buy_success, name='buy_success'),
    path('write_review/<int:product_id>/', write_review, name='write_review'),
]
