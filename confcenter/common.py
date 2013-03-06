__author__ = 'vs'
# -*- coding: utf-8 -*-
import inspect
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper


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

def return_file(infile, name):
    with open(infile) as f:
        content = f.read()
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=' + name
    return response
