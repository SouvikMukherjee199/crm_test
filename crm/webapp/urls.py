from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home' ),
    # path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('client/<int:pk>', views.client, name='client'),
    path('client_delete/<int:pk>', views.client_delete, name='client_delete'),
    path('add_client/', views.add_client, name='add_client'),
    path('client_update/<int:pk>', views.client_update, name='client_update'),
    path('client/product/<int:client_pk>/', views.product, name='product'),
    path('client/new_product/<int:client_pk>/', views.new_product, name='new_product'),
    path('search_client/', views.search_client, name='search_client'),
    path('client/delete_product/<int:product_pk>/', views.delete_product, name='delete_product'),

]
