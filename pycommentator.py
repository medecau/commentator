#!/usr/bin/python
# -*- coding: utf-8 -*-
#import webbrowser
from inspect import *

def doc(obj):
    '''document obj
    return a dictionary of the obj metadata'''
    current = dict()
    
    if obj.__name__:
        current['name']=obj.__name__
    elif obj.__file__:
        current['file']=obj.__file__
        
    
    if obj.__doc__:
        current['doc']=obj.__doc__
    else:
        current['doc']=None
    
    if isfunction(obj) or ismethod(obj):
        pass
    
    if isclass(obj):
        methods=getmembers(obj, ismethod)
        if len(methods)>0:
            current['methods']=list()
            for method in methods:
                current['methods'].append(doc(method[1]))
        else:
            current['methods']=None
    
    if ismodule(obj):
        functions=getmembers(obj, isfunction)
        if len(functions)>0:
            current['functions']=list()
            for function in functions:
                current['functions'].append(doc(function[1]))
        else:
            current['functions']=None
        classes=getmembers(obj, isclass)
        if len(classes)>0:
            current['classes']=list()
            for classie in classes:
                current['classes'].append(doc(classie[1]))
        else:
            current['classes']=None
    
    return current



def docs(module):
    '''Attempt to access the module
    '''
    try:
        obj = __import__(module)
        if ismodule(obj):
            return doc(obj)
        else:
            print 'Error: not a module'
    except ImportError:
        print 'Error: No such module could be imported'
    

