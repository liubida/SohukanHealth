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
    
    class Meta:
        db_table = 'app_available_data'
        ordering = ['-time', '-gmt_create']
        
#        app_label = '' # class not in app's models.py
#        abstract = True
        get_latest_by = "gmt_modify" # Entry.objects.latest()
#        managed = True #whether database table creation or deletion operations will be performed for this model
#        unique_together = ('user_id', 'name')
