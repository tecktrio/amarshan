

import json
from xml.dom import DOMException
from django.http import JsonResponse, QueryDict
from django.urls import resolve

from project_amarsha.settings import ACCESS_TOKEN_FOR_AMARSHAN_APP


class Authenticate_User_Middleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_counter = 0

    def __call__(self, request):
            # print(request.GET.get('access_token'))
            device=request.META['HTTP_USER_AGENT']
            request.device = device
            response = self.get_response(request)
            access_token = request.GET.get('access_token')
            if access_token == ACCESS_TOKEN_FOR_AMARSHAN_APP:
                return response
            else:
                return JsonResponse({'status':'access token does not match'})
            
    
            

    
 