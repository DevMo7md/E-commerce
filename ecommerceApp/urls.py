from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='main'),
    path('about/', views.about, name='about'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_user/', views.update_user, name='update_user'),
    path('update_pw/', views.update_pw, name='update_pw'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('cart_add/', views.cart_add, name='cart_add'),
    path('products/<int:pk>', views.products, name='products'),
    path('categorys/<str:foo>', views.category, name='categorys'),
    
    

]
