

from xml.dom import DOMException


class Authenticate_User_Middleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_counter = 0

    def __call__(self, request):
        # print(request.META['HTTP_USER_AGENT'])
        return self.get_response(request)
    
    def process_view(self,request, view_func, view_args, view_kwargs):
        # print(view_func.__name__,request)
        pass