__author__ = 'vs'
# -*- coding: utf-8 -*-
import inspect

def whoami():
    return inspect.stack()[1][3]

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_session_key(request):
    if request.session.session_key:
        return request.session.session_key
    else:
        return 'None'