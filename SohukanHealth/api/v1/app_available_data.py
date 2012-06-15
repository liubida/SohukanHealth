# -*- coding: utf-8 -*-
'''
Created on Jun 14, 2012

@author: liubida
'''

from djangorestframework.resources import ModelResource
from djangorestframework.tests import reverse
from monitor.models import AppAvailableData

class LineItemResource(ModelResource):  
    model =  AppAvailableData 
#    fields = ('name', 'time', 'time_used')
#    def product(self, instance):  
#        return instance

class read_data_resource(ModelResource):
    model =  AppAvailableData
    fields = ('name', 'time_used', 'day')
    
    def comments(self, instance):
        return reverse('comments', kwargs={'blogpost': instance.key})
    
    print AppAvailableData.objects.filter(name='read').values()
    model = AppAvailableData.objects.filter(name='read').values()
    
    