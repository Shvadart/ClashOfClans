# decorators.py
from functools import wraps
from collect import collect_resources_if_visible

def with_resource_collection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        collect_resources_if_visible()
        return func(*args, **kwargs)
    return wrapper