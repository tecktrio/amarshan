

from xml.dom import DOMException

from django.http import QueryDict


class Authenticate_User_Middleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_counter = 0

    def __call__(self, request):
        device = request.META['HTTP_USER_AGENT']
        # print(device)
        # q = QueryDict('', mutable=True)
        # q.update({'device': device})
        # request.POST = q

        response = self.get_response(request)
        return response
    
    def process_view(self,request, view_func, view_args, view_kwargs):
        # print(view_func.__name__,request)
        pass