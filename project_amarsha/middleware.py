

from xml.dom import DOMException

from django.http import QueryDict


class Authenticate_User_Middleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_counter = 0

    def __call__(self, request):
        device = request.META['HTTP_USER_AGENT']
       
        response = self.get_response(request)
        return response

    
 