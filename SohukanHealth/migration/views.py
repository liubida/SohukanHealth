#-*- coding: utf-8 -*-

'''
Created on May 19, 2013

@author: cescgao
'''

from config.config import c
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from statistics.models import *
from monitor.models import *
import datetime
import MySQLdb
import anyjson

def sys_alarm(request):
    try:
        conn = MySQLdb.connect(**c.db_self_config)
        cur = conn.cursor()
        raw_data = SysAlarm.objects.all()
        for d in raw_data:
            if not d.wiki_url:
                d.wiki_url = ''
            if not d.comments:
                d.comments = ''
            sql = '''insert into sys_alarm values("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");''' % (d.id, d.type, d.start_time, d.end_time, d.reason, d.wiki_url, d.comments, d.gmt_create, d.gmt_modify)
            cur.execute(sql)
        conn.commit()
    except Exception, e:
        c.logger.error(e)
    finally:
        try:
            cur.close()
        except Exception, e:
            c.logger.error(e)
        finally:
            if conn:
                conn.close()
    return HttpResponse('')

def stats_ua(request):
    try:
        conn = MySQLdb.connect(**c.db_self_config)
        cur = conn.cursor()
        raw_data = UA.objects.all()
        for d in raw_data:
            if d.is_crawler:
                d.is_crawler = '1'
            else:
                d.is_crawler = '0'
            sql = '''insert into stats_ua values("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");''' % (d.id, d.platform, d.os_version, d.majorver, d.minorver, d.browser, d.is_crawler, d.ua_string, d.gmt_create, d.gmt_modify)
            cur.execute(sql)
            conn.commit()
    except Exception, e:
        c.logger.error(e)
    finally:
        try:
            cur.close()
        except Exception, e:
            c.logger.error(e)
        finally:
            if conn:
                conn.close()
    return HttpResponse('')

def stats_opertype(request):
    try:
        conn = MySQLdb.connect(**c.db_self_config)
        cur = conn.cursor()
        raw_data = OperType.objects.all()
        for d in raw_data:
            d.name = ''
            sql = '''insert into stats_opertype values("%s", "%s", "%s", "%s", "%s", "%s");''' % (d.id, d.name, d.path, d.method, d.gmt_create, d.gmt_modify)
            cur.execute(sql)
            conn.commit()
    except Exception, e:
        c.logger.error(e)
    finally:
        try:
            cur.close()
        except Exception, e:
            c.logger.error(e)
        finally:
            if conn:
                conn.close()
    return HttpResponse('')

def app_available_data(request):
    try:
        conn = MySQLdb.connect(**c.db_self_config)
        cur = conn.cursor()
        raw_data = AppAvailableData.objects.all()
        for d in raw_data:
            d.category = ''
            if d.result:
                d.result = '1'
            else:
                d.result = '0'
            sql = '''insert into app_available_data values("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");''' % (d.id, d.name, d.category, d.result, d.time, d.time_used, d.comments, d.gmt_create, d.gmt_modify)
            cur.execute(sql)
            conn.commit()
    except Exception, e:
        c.logger.error(e)
    finally:
        try:
            cur.close()
        except Exception, e:
            c.logger.error(e)
        finally:
            if conn:
                conn.close()
    return HttpResponse('')

def aggregation(request):
    try:
        conn = MySQLdb.connect(**c.db_self_config)
        cur = conn.cursor()
        raw_data = Aggregation.objects.all()
        for d in raw_data:
            d.comments = ''
            d.content = d.content.replace('\\', '\\\\')
            d.content = d.content.replace('"', '\\"')
            sql = '''insert into aggregation values("%s", "%s", "%s", "%s", "%s", "%s", "%s");''' % (d.id, d.type, d.time, d.content, d.comments, d.gmt_create, d.gmt_modify)
            print d.id, d.type, d.time, d.content, d.comments, d.gmt_create, d.gmt_modify
            cur.execute(sql)
            conn.commit()
    except Exception, e:
        c.logger.error(e)
    finally:
        try:
            cur.close()
        except Exception, e:
            c.logger.error(e)
        finally:
            if conn:
                conn.close()
    return HttpResponse('')

def report(request):
    try:
        conn = MySQLdb.connect(**c.db_self_config)
        cur = conn.cursor()
        raw_data = Report.objects.all()
        for d in raw_data:
            d.comments = ''
            d.jsondata = d.jsondata.replace('\\', '\\\\')
            d.jsondata = d.jsondata.replace('"', '\\"')
            sql = '''insert into report values("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");''' % (d.id, d.type, d.time, d.version, d.jsondata, d.comments, d.gmt_create, d.gmt_modify)
            cur.execute(sql)
            conn.commit()
    except Exception, e:
        c.logger.error(e)
    finally:
        try:
            cur.close()
        except Exception, e:
            c.logger.error(e)
        finally:
            if conn:
                conn.close()
    return HttpResponse('')

def stats_oper(request):
    try:
        conn = MySQLdb.connect(**c.db_self_config)
        cur = conn.cursor()
        o = Oper.objects.all().order_by('-gmt_create')[0]
        print o.id, o.user_id, o.oper_type_id
        raw_data = Oper.objects.all()
        for d in raw_data:
            if not d.user_id:
                d.user_id = ''
            sql = '''insert into stats_oper values("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");''' % (d.id, d.user_id, d.oper_type_id, d.ua_id, d.remote_ip, '', d.gmt_create, d.gmt_modify)
            cur.execute(sql)
            conn.commit()
    except Exception, e:
        c.logger.error(e)
    finally:
        try:
            cur.close()
        except Exception, e:
            c.logger.error(e)
        finally:
            if conn:
                conn.close()
    return HttpResponse('')
