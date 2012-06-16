import sys
import os
import inspect
import pkgutil

class Commentator(object):
    def __init__(self, obj):
        self.obj = obj
    
    def __repr__(self):
        if self.isroutine:
            return '%s(%s)' % (self.name, self.formatedargs)
        if self.isclass:
            return '%s(%s)' % (self.name, self.init.formatedargs)
        return self.name
    
    @property
    def name(self):
        try:
            return self.obj.__name__
        except AttributeError:
            return str(type(self.obj))
    
    @property
    def doc(self):
        return inspect.getdoc(self.obj) or inspect.getcomments(self.obj)
    
    @property
    def file(self):
        return self.obj.__file__
    
    @property
    def members(self):
        for member in inspect.getmembers(self.obj):
            d = Commentator(member[1])
            if (d.isroutine or d.isclass or d.ismodule) and not d.isbuiltin:
                yield d
        
        for mod in self.modules:
            yield mod
    
    @property
    def modules(self):
        if self.ispackage:
            for member in pkgutil.iter_modules([os.path.dirname(self.file)]):
                yield comment(self.name+'.'+member[1])
    
    @property
    def classes(self):
        for member in self.members:
            if member.isclass:
                yield member
    
    @property
    def methods(self):
        for member in self.members:
            if member.ismethod:
                yield member
    
    @property
    def functions(self):
        for member in self.members:
            if member.isfunction:
                yield member
    
    @property
    def init(self):
        if self.isclass:
            for method in self.methods:
                if method.name == '__init__':
                    return method
    
    @property
    def argspec(self):
        if self.isroutine:
            return tuple(inspect.getargspec(self.obj))
    
    @property
    def formatedargs(self):
        args=self.args
        if self.defaults:
            args=args[:len(args)-len(self.defaults)]
            argsdef=self.args[len(args):]
        
        if self.ismethod:
            args=args[1:]
        
        
        args_list=args
        if self.defaults:
            args_list.extend(['%s=%s' % (k,v) for k in argsdef for v in self.defaults])
        if self.varargs:
            args_list.append('*%s' % self.varargs)
        if self.keywords:
            args_list.append('*%s' % self.keywords)

        return ', '.join(args_list)
    
    @property
    def args(self):
        return self.argspec[0]
    
    @property
    def varargs(self):
        return self.argspec[1]
    
    @property
    def keywords(self):
        return self.argspec[2]
    
    @property
    def defaults(self):
        return self.argspec[3]
    
    @property
    def ispackage(self):
        if self.ismodule:
            appendix = ['', 'c', 'o']
            file_path = self.obj.__file__

            for append in appendix:
                if file_path.endswith('__init__.py' + append):
                    return True
        return False
    
    @property    
    def ismodule(self):
        return inspect.ismodule(self.obj)
    
    @property
    def isclass(self):
        return inspect.isclass(self.obj)
    
    @property
    def ismethod(self):
        return inspect.ismethod(self.obj)
    
    @property
    def isfunction(self):
        return inspect.isfunction(self.obj)
    
    @property
    def isroutine(self):
        return inspect.isroutine(self.obj)
    
    @property
    def isbuiltin(self):
        return inspect.isbuiltin(self.obj)
    

def load_module(name):
    obj = __import__(name)
    mod_path=name.split('.')
    for sub in mod_path[1:]:
        obj = obj.__dict__.get(sub)
    return obj

def comment(name):
    obj = load_module(name)
    if inspect.ismodule(obj):
        return Commentator(obj)
    else:
        print 'Error: not a module'
