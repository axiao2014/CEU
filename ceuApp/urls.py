from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('create', views.create),
    path('add/<int:course_id>', views.add),
    path('drop/<int:course_id>', views.drop),
    path('destroy/<int:course_id>', views.destroy),
    path('contact', views.contact),
    path('about', views.about),
    path('logout', views.logout),
    path('home', views.home),
    path('cart', views.cart),
    path('purchase', views.purchase),
    path('config/', views.stripe_config),
    path('create-checkout-session/', views.create_checkout_session),
    path('success', views.success),
    path('cancelled/', views.cancelled),
]