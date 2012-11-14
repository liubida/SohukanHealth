from django.db import models

# Create your models here.

MAX_UA_LENGTH = 192

class Report(models.Model):
    
    type = models.CharField(max_length=64, blank=True, null=True)
    time = models.DateTimeField(db_index=True)
    version = models.IntegerField(blank=True, null=True)
    jsondata = models.TextField(blank=True, null=True)
    comments = models.CharField(max_length=512, blank=True, null=True)
    gmt_create = models.DateTimeField(auto_now_add=True, null=True)
    gmt_modify = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'report'
        ordering = ['time', 'gmt_create']
        get_latest_by = "time" # Entry.objects.latest()
        
class OperType(models.Model):
    
    name = models.CharField(max_length=128, null=True, blank=True)
    path = models.CharField(max_length=128, db_index=True)
    method = models.CharField(max_length=16, db_index=True)
    gmt_create = models.DateTimeField(auto_now_add=True, null=True)
    gmt_modify = models.DateTimeField(auto_now=True, null=True)
    
    def __unicode__(self):
        
        return u'%s %s' % (self.method, self.path)
    
    class Meta:
        unique_together = ('path', 'method')
        db_table = 'stats_opertype'
        ordering = ['gmt_create']


class Oper(models.Model):
    
    user_id = models.IntegerField(null=True, blank=True, db_index=True)
    oper_type_id = models.IntegerField(db_index=True)
    ua_id = models.IntegerField(db_index=True)
    remote_ip = models.CharField(max_length=128, null=True, blank=True)
    meta = models.TextField(blank=True, null=True)
    gmt_create = models.DateTimeField(auto_now_add=True, null=True)
    gmt_modify = models.DateTimeField(auto_now=True, null=True)
    
    def __unicode__(self):
        
        return u'id:%s performs action:%d' % (self.user_id, self.oper_type_id)

    class Meta:
        db_table = 'stats_oper'
        ordering = ['gmt_create']

class OperRaw(models.Model):
    
    user_id = models.IntegerField(null=True, blank=True, db_index=True)
    oper_id = models.IntegerField(db_index=True)
    request = models.TextField(blank=True, null=True)
    gmt_create = models.DateTimeField(auto_now_add=True, null=True)
    gmt_modify = models.DateTimeField(auto_now=True, null=True)
    
    def __unicode__(self):
        
        return u'%d' % self.oper_id
    
    class Meta:
        db_table = 'stats_operraw'
        ordering = ['gmt_create']

class OperObject(models.Model):
    
    user_id = models.IntegerField(null=True, blank=True, db_index=True)
    oper_id = models.IntegerField(db_index=True)
    object_type = models.CharField(max_length=32, db_index=True)
    object_key = models.CharField(max_length=4096, blank=True, null=True)
    gmt_create = models.DateTimeField(auto_now_add=True, null=True)
    gmt_modify = models.DateTimeField(auto_now=True, null=True)
    
    def __unicode__(self):
        
        return u'on type:%d id:%s' % (self.object_type, self.object_key)

    class Meta:
        db_table = 'stats_operobject'
        ordering = ['gmt_create']

class UA(models.Model):
    
    platform = models.CharField(max_length=32, db_index=True)
    os_version = models.CharField(max_length=32, db_index=True)
    majorver = models.CharField(max_length=32, db_index=True)
    minorver = models.CharField(max_length=32, db_index=True)
    browser = models.CharField(max_length=32, db_index=True)
    is_crawler = models.BooleanField()
    ua_string = models.CharField(max_length=MAX_UA_LENGTH)
    gmt_create = models.DateTimeField(auto_now_add=True, null=True)
    gmt_modify = models.DateTimeField(auto_now=True, null=True)
    
    def __unicode__(self):
        
        return u'%s' % self.ua_string
    
    class Meta:
        unique_together = ('ua_string',)
        db_table = 'stats_ua'
        ordering = ['gmt_create']

class Aggregation(models.Model):
    
    type = models.CharField(max_length=64, db_index=True)
    time = models.DateTimeField(db_index=True)
    content = models.TextField(blank=True, null=True)
    comments = models.CharField(max_length=512)
    gmt_create = models.DateTimeField(auto_now_add=True, null=True)
    gmt_modify = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        db_table = 'aggregation'
        ordering = ['time', 'gmt_create']
        get_latest_by = "time" # Entry.objects.latest()