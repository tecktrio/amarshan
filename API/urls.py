"""project_amarsha URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

from API import views

urlpatterns = [
    # root or about
    path('', views.root.as_view()),
    path('storage', views.Handle_Storage.as_view()),
    # Admin
    
    
    # User
    path('donations/<int:id>', views.Donation_content.as_view()),
    path('donations/filter/<str:category>', views.Donation_content.as_view()),
    path('donations/upload', views.Upload.as_view()),
    path('donations/categories',views.Handle_Donation_categories.as_view()),
    path('donations/categories/<int:id>',views.Handle_Donation_categories.as_view()),
    path('donations/history',views.Handle_Donation_History.as_view()),

    # featured entpoints to control the featured data in server
    path('featured', views.Featured_content.as_view()),
    path('featured/<int:id>', views.Featured_content.as_view()),
    path('signup',views.SignUp.as_view()),
    path('signup/<str:email_id>',views.SignUp.as_view()),
    path('login',views.Login.as_view()),
    path('trafficinfo',views.TrafficInfo.as_view()),
    path('email',views.Email.as_view()),
    path('address/<str:email_id>',views.Handle_Address.as_view()),
    path('payment/<str:email>',views.Handle_Payment.as_view()),
    # path('payment',views.Handle_Payment.as_view()),
    
    # Shopping
    #for post request ( add product )
    path('shopping/products',views.Handle_Products.as_view()),
    path('shopping/orders/<str:email_id>',views.Handle_myorders.as_view()),
    path('shopping/orders/edit/<str:order_id>',views.Handle_myorders.as_view()),
    # path('shopping/orders',views.Handle_Products.as_view()),
    #get request
    path('shopping/products/<str:filter>',views.Handle_Products.as_view()),
    path('shopping/categories',views.Handle_categories.as_view()),
    path('notifications',views.Handle_Notifications.as_view()),
    path('notifications/<int:id>',views.Handle_Notifications.as_view()),
    
    
]
