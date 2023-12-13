from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (home,
                    register, 
                    registration_success, 
                    products, 
                    detail_product, 
                    buy_success, 
                    write_review,
                    review_success, 
                    custom_login, 
                    custom_logout, 
                    CustomPasswordChangeView, 
                    CustomPasswordChangeDoneView
                   )

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('registration_success/', registration_success, name='registration_success'),
    path('products/', products, name='products'),
    path('detail/<int:product_id>/', detail_product, name='detail_product'),
    path('buy/success/<int:product_id>/', buy_success, name='buy_success'),
    path('write_review/<int:product_id>/', write_review, name='write_review'),
    path('review_success/', review_success, name='review_success'),
    path('custom_login/', custom_login, name='custom_login'),
    path('logout/', custom_logout, name='logout'),
    path('password-change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
]
