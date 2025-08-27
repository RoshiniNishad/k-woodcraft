from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('living-room/', views.living_room, name='living_room'),
    path('bedroom/', views.bedroom, name='bedroom'),
    path('dining-kitchen/', views.dining_kitchen, name='dining_kitchen'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('cart/', views.cart_view, name="cart"),
    path('add/<int:pk>/', views.add_to_cart, name="add_to_cart"),
    path('remove/<int:pk>/', views.remove_from_cart, name="remove_from_cart"),
    path('update/<int:pk>/', views.update_cart, name="update_cart"),
    path("payment/<int:pk>/", views.payment_view, name="payment"),
    path("payment/success/<int:pk>/", views.payment_success, name="payment_success"),
    path("checkout/", views.cart_checkout, name="cart_checkout"),

]
