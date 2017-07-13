#!/usr/bin/env python
#coding=utf8
import functools
import json

def json_output(decorated):
    """
    run the decorated function,return JSON string
    """
    @functools.wraps(decorated)
    def inner(*args,**kwargs):
        result = decorated(*args,**kwargs)
        return json.dumps(result)
    return inner

@json_output
def a():
    return {'333':3,'frf':323,'fewf':'fewf'}

print(a())
