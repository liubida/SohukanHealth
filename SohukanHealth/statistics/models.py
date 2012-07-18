from django.db import models

# Create your models here.

class DayReport(models.Model):
        
    time = models.DateTimeField(db_index=True)
    version = models.IntegerField(blank=True, null=True)
    jsondata = models.TextField(blank=True,null=True)
    comments = models.CharField(max_length=512, blank=True, null=True)
    gmt_create = models.DateTimeField(auto_now_add=True, null=True)
    gmt_modify = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'day_report'
        ordering = ['time', 'gmt_create']
        get_latest_by = "time" # Entry.objects.latest()
        
