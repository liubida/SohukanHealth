# -*- coding: utf-8 -*-
'''
Created on Jun 15, 2012

@author: liubida
'''
import anyjson

#class JSChart(object):
#     JSChart 

class Person(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age
        
    def __repr__(self):
        return 'Person Object [name:%s, age:%d]' % (self.name, self.age)

def object2dict(obj): 
    #convert object to a dict 
    d = {} 
    d['__class__'] = obj.__class__.__name__ 
    d['__module__'] = obj.__module__ 
    d.update(obj.__dict__) 
    return d 

def dict2object(d): 
    #convert dict to object 
    if '__class__' in d: 
        class_name = d.pop('__class__') 
        module_name = d.pop('__module__') 
        module = __import__(module_name) 
        class_ = getattr(module, class_name) 
        
        args = dict((key.encode('ascii'), value) for key, value in d.items()) #get args 
        
        inst = class_(**args) #create new instance 

    else: 
        inst = d 
    
    return inst 

if __name__ == '__main__': 
    p = Person('Peter', 22) 
    print p 

#    d = object2dict(p) 
#    o = dict2object(d) 


    dump = anyjson.dumps(p, default=object2dict) 
    print dump 
    #{"age": 22, "__module__": "Person", "__class__": "Person", "name": "Peter"} 

    load = anyjson.loads(dump, object_hook=dict2object) 
    print load.name #Person Object name : Peter , age : 22
    
