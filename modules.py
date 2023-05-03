import datetime
from django.core.mail import EmailMessage, get_connection
from boto3.session import Session
import os
import smtplib
import time
import threading
import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle

from API.models import User_Wallet
from API.models import Featured
from API.models import Users
from API.models import Products
from API.models import Categories
from API.models import Notification
from API.models import Donation_categories
from API.models import Donations
from API.models import Login_details

from API.serializers import User_Wallet_Serializer
from API.serializers import DonationContent_Serializer
from API.serializers import FeaturedContent_Serializer
from API.serializers import User_Serializer
from API.serializers import Product_Serializer
from API.serializers import Category_Serializer
from API.serializers import Donation_category_serializer
from API.serializers import Notification_serializer
from API.serializers import User_Address_Serializer
from API.models import Orders
from API.serializers import Order_Serializer
from API.models import Donation_History
from API.serializers import Donation_History_Serializer
from API.serializers import Login_Detail_Serializer
from API.models import Storage
from API.models import Donation_Payment
from API.serializers import Payment_Serializer
from project_amarsha.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME

from project_amarsha.settings import EMAIL_HOST_USER
from project_amarsha.settings import ACCESS_TOKEN_FACEBOOK_PAGE
from project_amarsha.settings import FACEBOOK_PAGE_ID
from project_amarsha.settings import INSTAGRAM_BUSINESS_ACCOUNT_ID

from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import JsonResponse
from django.shortcuts import render