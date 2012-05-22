#!/usr/bin/python
# -*- coding: utf-8 -*-
#import webbrowser
from json import dumps
from inspect import *
import os

def fput(content, file):
    fp=open(file, 'w+')
    fp.write(content)
    fp.close()

def doc_class(classie):
    out=do_doc(classie, 2)
    methods = getmembers(classie, ismethod)
    for method in methods:
        if not method[1].__name__.startswith('_'):
            out+=doc_method(method[1])
    return out

def doc_method(method):
    return do_doc(method, 3)

def doc_module(module):
    return do_doc(module, 1)

def doc_function(function):
    return do_doc(function, 3)

def doc_args(o):
    argspec= getargspec(o)
    argslist=list()
    if argspec[3]:
        args=argspec[0][:len(argspec[3])*-1]
    else:
        args=argspec[0]
    defargs=argspec[0][len(args):]
    optargs=list()
    for i,defarg in enumerate(defargs):
        optargs.append('%s=%s' % (defarg, argspec[3][i]))
    if argspec[1]:
        optargs.append('*args')
    if argspec[2]:
        optargs.append('**kwargs')
    if ismethod(o):
        out= ', '.join(args[1:])
    else:
        out= ', '.join(args)
    if len(optargs)>0:
        for i,optarg in enumerate(optargs):
            if i==0 and len(out)==0:
                out+='['
            else:
                out+='[, '
            out+=optarg
        out+=']'*len(optargs)
    return out

def do_doc(o, header=0):
    if ismethod and o.__name__=='__init__':
        out= '#'*header+' %s' % o.im_class.__name__
    else:
        out= '#'*header+' %s' % o.__name__
    if isfunction(o) or ismethod(o):
        out+= '(%s)' % doc_args(o)
    out+='\n'
    o_doc=getdoc(o)
    if o_doc:
        out+=o_doc
        out+='\n'
    out+='\n'
    return out


def extract_docs(module):
    
    # DOCUMENT THE MODULE
    # 
    docs=dict()
    docs['name'] = module.__name__
    docs['doc'] = module.__doc__
    #docs['file'] = module.__file__
    
    # DOCUMENT FUNCTIONS
    functions = getmembers(module, isfunction)
    if len(functions)>0:
        docs['functions'] = list()
        for name, function in functions:
            fdoc = dict()
            fdoc['name'] = function.__name__
            fdoc['doc'] = function.__doc__
            fdoc['args'] = getargspec(function)
            docs['functions'].append(fdoc)
    else:
        docs['functions'] = None
    
    # DOCUMENT CLASSES
    classes = getmembers(module, isclass)
    if len(classes)>0:
        docs['classes'] = list()
        for classie in classes:
            cdoc = dict()
            docs['classes'].append(cdoc)
    else:
        docs['classes'] = None
    '''
    classes = getmembers(module, isclass)
    for classie in classes:
        out+=doc_class(classie[1])
    #fput(out, module.__name__+'.md')
    print out
    '''
    return docs

def get_docs(module):
    try:
        object = __import__(module)
        if ismodule(object):
            return extract_docs(object)
        else:
            print 'Error: not a module'
    except ImportError:
        print 'Error: No such module could be imported'
    

