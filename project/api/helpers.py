from functools import wraps
import inspect
import json

from django.db import models
from django.http import JsonResponse, HttpResponse


class FlexibleJsonEncoder(json.JSONEncoder):
    '''Extends the JSON encoder to call __serialize__ on models and get serializable representation.

    Currently supports model instances and enumerables (such as lists, querysets).

    To pass arguments to the __serialize__ method, set the `serialize_args` argument
    of `json.dumps()` or any function that uses it internally.

    Example:
        ```
        class Article(models.Model):
            ...
            def __serialize__(self, capitalize_title=False):
                title = self.title
                if capitalize_title:
                    title = title.capitalize()
                return OrderedDict(title=title, content=self.content)

        articles = Article.objects.all()
        return JsonResponse(articles, encoder=FlexibleJsonEncoder, safe=False, serialize_args={
            'capitalize_title': True
        })
        ```
    '''
    def __init__(self, serialize_args=None, **kwargs):
        if serialize_args is None:
            serialize_args = {}
        self.serialize_args = serialize_args
        super().__init__(**kwargs)

    def default(self, o):
        # If the item is a Model
        if isinstance(o, models.Model):
            if callable(getattr(o, '__serialize__', None)):
                # For each argument in the object's __serialize__ method
                their_kwargs = inspect.signature(o.__serialize__).parameters.keys()
                # Omit kwargs that do not appear in self.serialize_args
                common_kwargs = [k for k in their_kwargs if k in self.serialize_args]
                # Get the corresponding value from serialize_args
                final = {k: self.serialize_args[k] for k in common_kwargs}
                return o.__serialize__(**final)
            # If the model does not have a __serialize__ method, return control to JSONEncoder
            # to raise TypeError
            return super().default(o)

        # If the item is not a Model, try iterating
        try:
            iterable = iter(o)
        except TypeError:
            pass
        else:
            # If item is iterable, get representation of each of the "children"
            # and add them to a list
            return [self.default(item) for item in iterable]

        # If all above fail, return control to JSONEncoder to raise TypeError
        return super().default(o)

def ApiResponse(data, **kwargs):
    '''Wrapper for JsonResponse that uses FlexibleJsonEncoder and UTF-8.

    The input data can also be a combination of native Python types and Django model
    instances.

    Example:
        ```
        data = {
            "start": 0,
            "count": 20,
            "articles": Article.objects.all()[:20]
        }
        return ApiResponse(data)
        ```
    '''
    kwargs.setdefault('json_dumps_params', {})
    kwargs['json_dumps_params']['ensure_ascii'] = False
    kwargs['encoder'] = FlexibleJsonEncoder
    kwargs['safe'] = False
    return JsonResponse(data, **kwargs)

def ApiMessage(msg, **kwargs):
    '''Returns JSON response {'message': msg} while maintaining UTF-8 encoding.

    Example:
        ```
        return ApiMessage('The field "title" is required.', status=400)
        ```

        Will return a 400 status code and {"message": "The field \"title\" is required."}
        as JSON content.
    '''
    kwargs.setdefault('json_dumps_params', {})
    kwargs['json_dumps_params']['ensure_ascii'] = False
    return JsonResponse({'message': msg}, **kwargs)


def user_is_volunteer(user):
    '''Check if user belongs in the Volunteer group or is admin.'''
    return user.is_authenticated and (
        user.is_staff or
        user.groups.filter(name='Volunteer').exists()
    )

def is_volunteer(request):
    '''Checks if the logged in user has Volunteer permissions'''
    return hasattr(request, 'user') and user_is_volunteer(request.user)


def volunteer_required(function=None):
    '''
    Decorator for views that checks that the user is a volunteer,
    i.e. can create or update entries in the observatory.
    '''
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if is_volunteer(request):
                return view_func(request, *args, **kwargs)
            return HttpResponse('Unauthorized', status=401)
        return _wrapped_view

    if function:
        return decorator(function)
    return decorator

def user_is_admin(user):
    return user.is_authenticated and user.is_staff

def is_admin(request):
    '''Checks if the logged in user has Admin permissions'''
    return hasattr(request, 'user') and user_is_admin(request.user)

def admin_required(function=None):
    '''
    Decorator for views that checks that the user is a staff member,
    i.e. can login to the administration interface and is thus able
    to create, update or delete resources.
    '''
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if is_admin(request):
                return view_func(request, *args, **kwargs)
            return HttpResponse('Unauthorized', status=401)
        return _wrapped_view

    if function:
        return decorator(function)
    return decorator
