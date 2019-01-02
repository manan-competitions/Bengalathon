"""portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index,  name='index'),
    path('customer/view/<int:pk>/', views.get_serialized_customer,  name='view_customer'),
    path('customer/add/', views.add_customer,  name='add_customer'),
    path('customer/edit/<int:pk>/', views.edit_customer,  name='edit_customer'),
    path('customer/edit/', views.edit_customer,  name='edit_customer_get'),
    path('customer/delete/<int:pk>/', views.delete_customer,  name='delete_customer'),
    path('accounts/register/', views.company_register, name='company_register'),
    path('accounts/login/', views.company_login, name='company_login'),
    path('accounts/logout/', views.company_logout, name='company_logout'),
]
