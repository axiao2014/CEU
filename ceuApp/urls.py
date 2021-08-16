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
    path('logout', views.logout),
]