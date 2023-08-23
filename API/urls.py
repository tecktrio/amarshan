
'''
urls for handling requests for amarshan app
'''

from django.contrib import admin
from django.urls import path

from API import views

urlpatterns = [
    # root or about
    path('', views.root.as_view()),
    
    # handle storage urls
    path('storage', views.Handle_Storage.as_view()),

    # handle donation urls
    path('donations/<int:id>',              views.Donation_content.as_view()),
    path('donations/filter/<str:filter>',   views.Donation_content.as_view()),
    path('donations/upload',                views.Upload.as_view()),
    path('donations/categories',            views.Handle_Donation_categories.as_view()),
    path('donations/categories/<int:id>',   views.Handle_Donation_categories.as_view()),
    path('donations/history',               views.Handle_Donation_History.as_view()),

    # handles featured urls
    path('featured',            views.Featured_content.as_view()),
    path('featured/<int:id>',   views.Featured_content.as_view()),
    
    # handle signup urls
    path('signup',                  views.SignUp.as_view()),
    path('updateprofile/<str:email_id>',                  views.SignUp.as_view()),
    
    # handling login urls
    path('login',views.Login.as_view()),
    path('changepassword/<str:email>',views.Handle_User_Change_Password.as_view()),
    
    # handling trafficinfo
    path('trafficinfo',views.TrafficInfo.as_view()),
    
    # handling email urls
    path('email',views.Email.as_view()),
    
    # handling address urls
    path('address/<str:email_id>',views.Handle_Address.as_view()),
    
    # handling payment urls
    path('payment/<str:email>',views.Handle_Payment.as_view()),
    path('withdraw',views.Handle_WidthDraw.as_view()),
    path('withdraw/<str:id>/<str:status>',views.Handle_WidthDraw.as_view()),
    path('wallet/<str:email>',views.Handle_User_Wallet.as_view()),
    
    #f handling shop urls
    path('shopping/products',                   views.Handle_Products.as_view()),
    path('shopping/orders/<str:email_id>',      views.Handle_myorders.as_view()),
    path('shopping/orders/edit/<str:order_id>', views.Handle_myorders.as_view()),
    
    # handling shopping  urls
    path('shopping/products/<str:filter>',  views.Handle_Products.as_view()),
    path('shopping/categories',             views.Handle_categories.as_view()),
    
    # handling notifications urls
    path('notifications',           views.Handle_Notifications.as_view()),
    path('notifications/<int:id>',  views.Handle_Notifications.as_view()),
    
    path('bank',  views.Handle_Bank_Accounts.as_view()),
    path('bank/<str:email_id>',  views.Handle_Bank_Accounts.as_view()),
    
    
    
    
]
