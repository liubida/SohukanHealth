# -*- coding: utf-8 -*-
'''
Created on Jun 7, 2012

@author: liubida
'''
import sys
import os
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print root_path
sys.path.append(root_path)
print sys.path

from django.core.management import setup_environ
from SohukanHealth import settings, aggregation
print settings
setup_environ(settings)

from config.config import c
from monitor.models import AppAvailableData, SomeTotal, SysAlarm
from monitor.system.worker import add_worker, read_worker
from statistics.biz import get_userdata_for_day_report, get_bookmark_website, get_bookmark_website_detail, \
    get_bookmarkdata_for_day_report, get_bookmark_percent_raw_data, _is_test, get_week_report_add_way_and_platform
from statistics.models import Report, UA
from timer.sms import sms
from util import print_info, query_ua, timediff, read_file, get_date_and_time
from util.random_spider import RandomSpider
import MySQLdb
import anyjson
import datetime


#@print_info(name='read_job')
def read_job():
    value = read_worker(c.cookie).test()
    data = AppAvailableData(name='read', category='', result=value.get('result', False), \
                            time=datetime.datetime.now(), time_used=value.get('time_used', c.read_time_limit), \
                            comments=value.get('comments', ''))
    data.save()
    return value

#@print_info(name='add_job')
def add_job():
    url = RandomSpider().get_valid_url()
    value = add_worker(url, c.cookie).test()
    data = AppAvailableData(name='add', category='', result=value.get('result', False), \
                            time=datetime.datetime.now(), time_used=value.get('time_used', c.add_time_limit), \
                            comments=value.get('comments', url))
    data.save()
    print '1:', value
    return value

@print_info(name='user_total_job')
def user_total_job(now=None):
    try:
        # TODO: there should be a dbhelper
        conn = MySQLdb.connect(**c.db_config)
        cursor = conn.cursor()

        #去掉测试用户的id
        tmp = ' where id !='
        tmp += ' and id !='.join(map(lambda x:str(x), c.test_id))
        
        # 今天
        if not now:
            now = datetime.datetime.now()
        now_str = now.strftime('%Y-%m-%d %H:%M:%S')
        
        sql = "select count(*) from account_user %s and (gmt_create is null or gmt_create <='%s')" % (tmp, now_str)
        print sql
        cursor.execute(sql)
        result = cursor.fetchone()
        
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

@print_info(name='shorturl_total_job')
def shorturl_total_job(now=None):
    try:
        # TODO: there should be a dbhelper
        conn = MySQLdb.connect(**c.db_self_config)
        cursor = conn.cursor()

        # 今天
        if not now:
            now = datetime.datetime.now()
        now_str = now.strftime('%Y-%m-%d %H:%M:%S')
        
        sql = "select count(*) from stats_oper o, stats_opertype t where o.oper_type_id = t.id and t.path = '/j/'"
        print sql
        cursor.execute(sql)
        result = cursor.fetchone()
        
        data = SomeTotal(name='shorturl', time=now, count=result[0])
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

@print_info(name='set_public_total_job')
def set_public_total_job(now=None):
    try:
        # TODO: there should be a dbhelper
        conn = MySQLdb.connect(**c.db_self_config)
        cursor = conn.cursor()

        # 今天
        if not now:
            now = datetime.datetime.now()
        now_str = now.strftime('%Y-%m-%d %H:%M:%S')
        
        sql = "select count(*) from stats_oper s, stats_operobject o, stats_opertype t where s.oper_type_id=t.id and s.id=o.oper_id and (t.id=64 or t.id=65 or t.id=67)"
        print sql
        cursor.execute(sql)
        result = cursor.fetchone()
        
        data = SomeTotal(name='set-public', time=now, count=result[0])
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
def bookmark_total_job(now=None):
    try:
        conn = MySQLdb.connect(**c.db_config)
        cursor = conn.cursor()
        
        # 今天
        if not now:
            now = datetime.datetime.now()
        now_str = now.strftime('%Y-%m-%d %H:%M:%S')
        
        remove_guide = " url not regexp '^http://kan.sohu.com/help/guide-' "
        sum = 0
        for i in range(64):
            sql = "select user_id, count(*) from bookmark_bookmark_%s where %s and \
            (gmt_create is null or gmt_create <= '%s') group by user_id" % (i, remove_guide, now_str)
            cursor.execute (sql)
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

@print_info(name='add_alarm_job')
def add_alarm_job():
    start_time = datetime.datetime.now() - datetime.timedelta(minutes=36) 
    add_failure_data = AppAvailableData.objects.filter(name='add', result=False, time__gte=start_time).values('time')
    failure_count = len(add_failure_data)
    
    if failure_count >= c.add_alarm_time: 
        try:
            start_time = add_failure_data[0]['time']
            end_time = add_failure_data[failure_count - 1]['time']
            type = 'add_bookmark'
            time = get_date_and_time()[1]
            msg = 'add failure count: %s,%s' % (str(failure_count), time)
            sms(mobile_list=c.mobile_list, message_post=msg)

            latest = SysAlarm.objects.filter(type=type).order_by('-gmt_create')
            if latest:
                latest = latest[0]
                # start_time是本次报警的开始时间
                # latest.end_time是上次报警的结束时间
                # 所有在算时间差的时候, start_time应该是时间差的end, latest.end_time应该是时间差的start
                tdiff = timediff(latest.end_time, start_time)
                if (not latest) or start_time > latest.end_time and tdiff > 600:
                    # 一次新故障
                    alarm = SysAlarm(type=type, start_time=start_time, end_time=end_time)
                    alarm.save()
                else:
                    # 添加-报警的定时任务是每10min执行一次, 如果本次报警的时间和上次开始的时间<10min, 则认为是同一次故障
                    # 同一次故障的持续报警, 只需修改上次的结束时间即可
                    latest.end_time = end_time
                    latest.save()
            else:
                # 以前没有过这样类型的故障
                alarm = SysAlarm(type=type, start_time=start_time, end_time=end_time)
                alarm.save()
        except Exception, e:
            c.logger.error(e)

@print_info(name='read_alarm_job')
def read_alarm_job():
    start_time = datetime.datetime.now() - datetime.timedelta(minutes=36) 
    read_failure_data = AppAvailableData.objects.filter(name='read', result=False, time__gte=start_time).values('time')
    failure_count = len(read_failure_data)
    
    if failure_count >= c.read_alarm_time: 
        try:
            start_time = read_failure_data[0]['time']
            end_time = read_failure_data[failure_count - 1]['time']
            type = 'read_bookmark'
            time = get_date_and_time()[1]
            msg = 'read failure count:%s,%s' % (str(failure_count), time)
            sms(mobile_list=c.mobile_list, message_post=msg)

            # 获取上一次的报警信息
            latest = SysAlarm.objects.filter(type=type).order_by('-gmt_create')
            if latest:
                latest = latest[0]
                # start_time是本次报警的开始时间
                # latest.end_time是上次报警的结束时间
                # 所有在算时间差的时候, start_time应该是时间差的end, latest.end_time应该是时间差的start
                tdiff = timediff(latest.end_time, start_time)
                if (not latest) or start_time > latest.end_time and tdiff > 600:
                    # 一次新的故障
                    alarm = SysAlarm(type=type, start_time=start_time, end_time=end_time)
                    alarm.save()
                else:
                    # 添加-报警的定时任务是每10min执行一次, 如果本次报警的时间和上次开始的时间<10min, 则认为是同一次故障
                    # 同一次故障的持续报警, 只需修改上次的结束时间即可
                    latest.end_time = end_time
                    latest.save()
            else:
                # 以前没有过这样类型的故障
                alarm = SysAlarm(type=type, start_time=start_time, end_time=end_time)
                alarm.save()
        except Exception, e:
            c.logger.error(e)

@print_info(name='rabbitmq_queue_alarm_job')
def rabbitmq_queue_alarm_job():
    queue = {'log': None, 'purify': None, 'upload': None, 'download': None,
             'encode': None, 'entry': None, 'store': None}
    try:
        # lines should be only one row
        lines = read_file("/tmp/rabbitmq_queue.o")
        if not lines:
            c.logger.error("/tmp/rabbitmq_queue.o is blank")
            
        info = lines[0]
#        info = r"encode:|entry:|purify:|download:|log:|upload:|store:"
        
        item_list = info.split('|')
        if not item_list:
            c.logger.error("queue_info parse error")
        
        for item in item_list:
            tmp = item.split(':')
            if tmp[1] and tmp[1] != '\n':
                queue[tmp[0]] = int(tmp[1])
    
        error_q = []
        for q in queue.keys():
            if q == 'log':
                if queue[q] is None or queue[q] >= 128:
                    error_q.append("%s:%s" % (q, queue[q]))
            else:
                if queue[q] is None or queue[q] >= 32:
                    error_q.append("%s:%s" % (q, queue[q]))
        
        if error_q:
            time = get_date_and_time()[1]
            content = '|'.join(error_q)
            msg = '[%s] %s' % (time, content)
            sms(mobile_list=c.mobile_list, message_post=msg)
    except Exception, e:
        c.logger.error(e)
        
@print_info(name='day_report_job')
def day_report_job(now=None):
    '''day_report created at 23:58:00'''
    
    # 今天
    if not now:
        now = datetime.datetime.now()
    
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = now.replace(hour=23, minute=59, second=59, microsecond=0)
    
    user = get_userdata_for_day_report(today_start, today_end);
    bookmark = get_bookmarkdata_for_day_report(today_start, today_end);
    
    bookmark_count = {}
    bookmark_count['percent'], bookmark_count['data'] = get_bookmark_percent_raw_data(today_start, today_end, limit=20)
    bookmark_website = {}
    bookmark_website['data'] = get_bookmark_website(today_start.strftime('%Y-%m-%d %H:%M:%S'), today_end.strftime('%Y-%m-%d %H:%M:%S'), limit=20)
    
    jsondata = {}
    jsondata['user'] = user
    jsondata['bookmark'] = bookmark
    jsondata['bookmark_website'] = bookmark_website
    jsondata['bookmark_count'] = bookmark_count
    
    day_report = Report(type='day', time=now, version=c.report_version, jsondata=anyjson.dumps(jsondata))
    day_report.save();

@print_info(name='week_report_job')
def week_report_job(today=None):
    '''week_report created at mon 07:00:00'''
    
    if not today:
        today = datetime.date.today()
    # 双重保证, 不是周一就返回
    if today.isoweekday() != 1:
        return
    # 从上周的周一开始 
    last_mon = today - datetime.timedelta(days=7)
    start_time = datetime.datetime(last_mon.year, last_mon.month, last_mon.day)
    start_time = start_time.replace(hour=0, minute=0, second=0, microsecond=0)
    jsondata_array = Report.objects.filter(type='day', time__gte=start_time, time__lt=today).values('jsondata')
    
    new_user = {}
    new_bookmark = {}
    failed_bookmark = {}
    if jsondata_array:
        count = 1
        for jsondata in jsondata_array:
            data = anyjson.loads(jsondata['jsondata'])
            # 本周每天新增用户
            new_user[count] = data['user']['total'] - data['user']['total_yd']
            # 本周每天新增文章
            new_bookmark[count] = data['bookmark']['total'] - data['bookmark']['total_yd']
            # 本周每天失败文章
            try:
                each_failed_bookmark = data['bookmark']['failed']
            except Exception:
                each_failed_bookmark = []

            failed_bookmark[count] = {'count':len(each_failed_bookmark), 'data': each_failed_bookmark}
            count = count + 1
    end_time = start_time + datetime.timedelta(days=6)
    end_time = end_time.replace(hour=23, minute=59, second=59, microsecond=0)
    
    bookmark_website = {}
    bookmark_website['data'] = get_bookmark_website_detail(start_time.strftime('%Y-%m-%d %H:%M:%S'), \
                                                           end_time.strftime('%Y-%m-%d %H:%M:%S'), limit=100, urls_limit=50)

    add_way_and_platform = {}
    add_way_and_platform['data'] = get_week_report_add_way_and_platform(start_time, end_time);
    
    jsondata = {}
    jsondata['new_user'] = new_user
    jsondata['new_bookmark'] = new_bookmark
    jsondata['failed_bookmark'] = failed_bookmark
    jsondata['bookmark_website'] = bookmark_website
    jsondata['add_way_and_platform'] = add_way_and_platform

    week_report = Report(type='week', time=today, version=c.report_version, jsondata=anyjson.dumps(jsondata))
    week_report.save();
    
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

@print_info(name='day_aggregation')
def day_aggregation_job(start_time=datetime.datetime.now()):
    try:
        aggregation.share_channels(start_time)
        aggregation.public_client(start_time)
        aggregation.activate_user(start_time)
        aggregation.bookmark_website(start_time)
        aggregation.user_platform(start_time)
    except Exception, e:
        c.logger.error(e)
        
if __name__ == '__main__':
#<<<<<<< HEAD
    #add_job()
    #exit
#    start = datetime.datetime(2012, 12, 21, 6, 52, 0)
#    start = datetime.datetime(2012, 11, 16, 6, 58, 0)
#    step = datetime.timedelta(days=1)
#    
#    now = datetime.datetime.now()
#    while start <= now:
        #day_aggregation_job(start)
        #day_report_job(start)
#        week_report_job(start)
#        start += step

#    add_job_monitor()
#=======
    pass

    # 重新跑 total 的数据
#    start = datetime.datetime(2013, 1, 9, 23, 59, 59)
#    print start
#    user_total_job(start);
#    bookmark_total_job(start);

#>>>>>>> cb9203f53cf9b4eb891fbbcccb0c102e54784cae

    # 重新跑 聚合/日报/周报 的数据
#    start = datetime.datetime(2013, 1, 9, 23, 59, 59)
#    step = datetime.timedelta(days=1)
#    
#    now = datetime.datetime.now()
#    while start <= now:
#        day_aggregation_job(start)
#        day_report_job(start)
#        week_report_job(start)
#        start += step
