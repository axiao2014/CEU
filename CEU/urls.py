"""CEU URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from django.contrib import admin
from ceuApp.models import User as U, Course, Order

class UAdmin(admin.ModelAdmin):
    pass 
admin.site.register(U, UAdmin)

class CourseAdmin(admin.ModelAdmin):
    pass 
admin.site.register(Course,CourseAdmin)

class OrderAdmin(admin.ModelAdmin):
    pass
admin.site.register(Order,OrderAdmin)

# class BillingAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(Billing,BillingAdmin)

urlpatterns = [
    path('', include('ceuApp.urls')),
    path('admin/',admin.site.urls),
]
