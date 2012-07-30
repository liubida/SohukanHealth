# -*- coding: utf-8 -*-
'''
Created on Jun 7, 2012

@author: liubida
'''

from config.config import c
from monitor.models import AppAvailableData, SomeTotal
from monitor.system.worker import add_worker, read_worker
from statistics.biz import get_userdata_for_day_report, \
    get_bookmarkdata_for_day_report, get_bookmark_website_raw_data, \
    get_bookmark_percent_raw_data, test_id, _is_test
from statistics.models import DayReport, UA
from timer.sms import sms
from util import print_info, query_ua
from util.random_spider import RandomSpider
import MySQLdb
import anyjson
import datetime

@print_info(name='read_job')
def read_job():
    value = read_worker(c.cookie).test()
    data = AppAvailableData(name='read', category='', result=value.get('result', False), \
                            time=datetime.datetime.now(), time_used=value.get('time_used', c.read_time_limit), \
                            comments=value.get('comments', ''))
    data.save()
    return value

@print_info(name='add_job')
def add_job():
    url = RandomSpider().get_valid_url()
    value = add_worker(url, c.cookie).test()
    data = AppAvailableData(name='add', category='', result=value.get('result', False), \
                            time=datetime.datetime.now(), time_used=value.get('time_used', c.add_time_limit), \
                            comments=value.get('comments', url))
    data.save()
    return value

@print_info(name='user_total_job')
def user_total_job():
    try:
        # TODO: there should be a dbhelper
        conn = MySQLdb.connect(**c.db_config)
        cursor = conn.cursor()

        #去掉测试用户的id
        tmp = ' where id > 100 and id !='
        tmp += ' and id !='.join(map(lambda x:str(x), test_id))
        print tmp
        cursor.execute('select count(*) from account_user %s' % tmp)
        result = cursor.fetchone()
        now = datetime.datetime.now()
        data = SomeTotal(name='user', time=now, count=result[0])
        data.save()
        return result[0]
    except Exception, e:
        c.logger.error(e)
        return str(e)
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception, e:
            c.logger.error(e)
        finally:
            if conn:
                conn.close()

@print_info(name='bookmark_total_job')
def bookmark_total_job():
    try:
        conn = MySQLdb.connect(**c.db_config)
        cursor = conn.cursor()
        sum = 0
        for i in range(64):
            cursor.execute ("select user_id, count(*) from bookmark_bookmark_%s group by user_id" % i)
            results = cursor.fetchall()
            for d in results:
                user_id = int(d[0])
                count = int(d[1])
                # 去掉测试用户添加的文章
                if not _is_test(user_id):
                    sum += count
        now = datetime.datetime.now()
        data = SomeTotal(name='bookmark', time=now, count=sum)
        data.save()
        return sum
    except Exception, e:
        c.logger.error(e)
        return str(e)
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception, e:
            c.logger.error(e)
        finally:
            if conn:
                conn.close()

@print_info(name='add_and_read_alarm_job')
def add_and_read_alarm_job():
    now = datetime.datetime.now()
    delta = datetime.timedelta(hours=0.5)
    start_time = now - delta
    print start_time
    
    add_failure_data = AppAvailableData.objects.filter(name='add', result=False, time__gte=start_time).count()
    read_failure_data = AppAvailableData.objects.filter(name='read', result=False, time__gte=start_time).count()
    
    if add_failure_data >= 3 or read_failure_data >= 3:
        msg = 'add bookmark failure count(30min):%s' % str(add_failure_data)
        msg += '\nread bookmark failure count(30min):%s' % str(read_failure_data)
        sms(mobile_list=c.mobile_list, message_post=msg)
        c.logger.error(msg)
        print msg

@print_info(name='day_report_job')
def day_report_job():
    '''day_report created at 23:58:00'''
    
    # 今天
    now = datetime.datetime.now()
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = now.replace(hour=23, minute=59, second=59, microsecond=0)
    
    user = get_userdata_for_day_report(today_start, today_end);
    bookmark = get_bookmarkdata_for_day_report(today_start, today_end);
    
    bookmark_count = {}
    bookmark_count['percent'], bookmark_count['data'] = get_bookmark_percent_raw_data(today_start, today_end)
    
    bookmark_website = {}
    bookmark_website['data'] = get_bookmark_website_raw_data(today_start, today_end)
    
    jsondata = {}
    jsondata['user'] = user
    jsondata['bookmark'] = bookmark
    jsondata['bookmark_website'] = bookmark_website
    jsondata['bookmark_count'] = bookmark_count
    
    day_report = DayReport(time=datetime.datetime.now(), version=c.day_report_version, jsondata=anyjson.dumps(jsondata))
    day_report.save();
    
@print_info(name='fix_ua_job')
def fix_ua_job():
    try:
        ua = UA.objects.filter(is_crawler=False)
        for u in ua:
            if u.ua_string.startswith(u'搜狐随身看'):
                u.platform = 'Darwin'
                u.is_crawler = True
            else:
                ret = query_ua(u.ua_string)
                if ret:
                    u.platform = ret['os_type']
                    u.is_crawler = True
            u.save()
    except Exception, e:
        c.logger.error(e)

if __name__ == '__main__':
    read_job()
#    add_job()
#    day_report_job()
#    today = datetime.date.today()
#    today = today.replace(day=31)
#    print today
#    d = datetime.timedelta(days=1)
#    print today + d
#    
#    fix_ua_job()
#    mysql_ping_job();
#    user_total_job()
#    bookmark_total_job()
#    add_and_read_alarm_job()
#    url = RandomSpider().get_valid_url()
