#!/usr/bin/python
# -*- coding: utf-8 -*-
VERSION=0.0


def document_module(module):
    import inspect
    try:
        module4docs=__import__(module)
        members = inspect.getmembers(module4docs)
        for member in members:
            print member
    except ImportError:
        print 'Error: No such module could be imported'
    


def main(argv):
    if len(argv)<2:
        print 'Error: No module defined'
        print 'Usage: %s <module>' % sys.argv[0]
    elif len(argv)>2:
        print 'Error: Only one module accepted'
        print 'Usage: %s <module>' % sys.argv[0]
    else:
        document_module(argv[1])
        
if __name__ == '__main__':
    import sys
    main(sys.argv)
