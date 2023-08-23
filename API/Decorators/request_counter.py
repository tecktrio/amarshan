# decorators.py

from functools import wraps
from django.core.cache import cache

def request_counter(view_func):
    print("Response from decorator")
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        # Get the current request count from the cache
        request_count = cache.get('request_count', 0)

        # Increment the request count
        request_count += 1

        # Store the updated request count in the cache
        cache.set('request_count', request_count)

        # Call the original view function
        response = view_func(request, *args, **kwargs)
        print("Response from decorator:", response)
        return response

    return wrapped_view
