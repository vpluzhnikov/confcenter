__author__ = 'vs'
# -*- coding: utf-8 -*-
import inspect

def whoami():
    return inspect.stack()[1][3]
