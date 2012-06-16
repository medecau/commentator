'''
test()
blablabla
'''

def _hidden_func(yo):
    pass

def test(var, var2, var3, **kwargs):
    '''Test function.'''
    return True

def test2(lol,roflol=True, *args):
    return True

def test3(lol, roflol=True, *args, **kwargs):
    return True

def test4(lol, roflol=True, lmfao=False, *args, **kwargs):
    return True

class Example(object):
    '''Example class documentation.'''
    pass
    def __init__(self, desc):
        self.var='haha'
    
    def do(self, lol, wtf=True):
        '''print var'''
        print self.var