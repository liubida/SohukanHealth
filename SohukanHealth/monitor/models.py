# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

class AppAvailableData(models.Model):

    name = models.CharField(max_length=64, db_index=True)
    category = models.CharField(max_length=64, db_index=True, blank=True, null=True)
    result = models.NullBooleanField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    time_used = models.IntegerField(blank=True, null=True)
    comments = models.CharField(max_length=512, blank=True, null=True)
    gmt_create = models.DateTimeField(auto_now_add=True, null=True)
    gmt_modify = models.DateTimeField(auto_now=True, null=True)
    
    def __unicode__(self):
        return u'%s' % self.name
    
    def get_full_name(self):
        "Returns the person's full name."
        return 'hello'
    
    class Meta:
        db_table = 'app_available_data'
        ordering = ['time', 'gmt_create']
        
#        app_label = '' # class not in app's models.py
#        abstract = True
        get_latest_by = "gmt_modify" # Entry.objects.latest()
#        managed = True #whether database table creation or deletion operations will be performed for this model
#        unique_together = ('user_id', 'name')

class SomeTotal(models.Model):
    name = models.CharField(max_length=64, db_index=True)
    time = models.DateTimeField(blank=True, null=True)
    count = models.BigIntegerField(blank=True, null=True)
    comments = models.CharField(max_length=512, blank=True, null=True)
    gmt_create = models.DateTimeField(auto_now_add=True, null=True)
    gmt_modify = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'some_total'
        ordering = ['time', 'gmt_create']
        get_latest_by = "gmt_modify" # Entry.objects.latest()
    
class UserRegister(models.Model):
    passport = models.CharField(max_length=128, db_index=True)
    time = models.DateTimeField(blank=True, null=True)
    comments = models.CharField(max_length=512, blank=True, null=True)
    gmt_create = models.DateTimeField(auto_now_add=True, null=True)
    gmt_modify = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        db_table = 'user_register'
        ordering = ['-time', '-gmt_create']
        get_latest_by = "gmt_modify" # Entry.objects.latest()
    
