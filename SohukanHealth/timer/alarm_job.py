# -*- coding: utf-8 -*-
'''
Created on Nov 28, 2012

@author: liubida
'''

from config.config import c
from lxml import html
from timer.sms import sms
from util import print_info, read_file
import datetime
import os
import requests
import sys
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)


@print_info(name='nginx_tcp_check_job')
def nginx_tcp_check_job(count=3):
    now = datetime.datetime.now()
    if now.hour == 7:
        c.redis_instance.delete(c.nginx_tcp_alarm_key)

    if count <= 0 :
        c.logger.error(datetime.datetime.strftime(now, '%Y-%m-%d %H:%M:%S') + ' nginx_tcp_check retry 3 times')
        sms(mobile_list=c.mobile_list, message_post='nginx_tcp_check retry 3 times')
        return
    
    need_alarm = False
    msg = ''
    try:
        print c.ha_nginx_check_url
        r = requests.get(c.ha_nginx_check_url, timeout=2)
        r.raise_for_status()
        s = html.fromstring(r.text, None, parser=html.HTMLParser(remove_blank_text=True))
        ip_list = s.xpath('//table/tr/td[2]')
        state_list = s.xpath('//table/tr/td[3]')
        
        tcp_check_status = []
        i = 0
        for ip in ip_list:
            tcp_check_status.append({'ip':ip.text_content(), 'state':state_list[i].text_content()})
            i = i + 1
        
        for s in tcp_check_status:
            msg = '%s|%s:%s' % (msg, s['ip'], s['state'])
            if s['state'] != 'up':
                need_alarm = True
    except Exception, e:
        now = datetime.datetime.now()
        c.logger.error('%s %s' % (str(datetime.datetime.strftime(now, '%Y-%m-%d %H:%M:%S')), str(e)))
        count = count - 1
        nginx_tcp_check_job(count);
    else:
        print 'msg:', msg
        if need_alarm:
            s = c.redis_instance.incr(c.nginx_tcp_alarm_key)
            if s <= c.max_nginx_tcp_alarm:
                sms(mobile_list=c.mobile_list, message_post=msg)
            c.logger.error('%s %s' % (str(datetime.datetime.strftime(now, '%Y-%m-%d %H:%M:%S')), msg))
        

@print_info(name='web_alarm_job')
def web_alarm_job():
    kan_url = 'http://kan.sohu.com/'
    reader_url = 'http://kan.sohu.com/reader/'
    MAX_ALARM_COUNT = 8
    
    now = datetime.datetime.now()
    now_str = datetime.datetime.strftime(now, '%Y-%m-%d %H:%M:%S')
    if int(now.hour) % 2 == 0:
        c.redis_instance.delete(c.web_alarm_key)

    #if count <= 0 :
    #    c.logger.error(now_str + ' web_check retry 3 times')
    #    sms(mobile_list=c.mobile_list, message_post='web_check retry 3 times')
    #    return
    
    need_alarm = False
    msg = ''
    msg_kan = 'kan is error'
    msg_reader = 'reader is error'
    msg_exception = 'checking kan/reader throws exception'
    try:
        r = requests.get(kan_url, timeout=60)
        if r.status_code != 200:
            need_alarm = True
            msg = '[%s]%s' % (now_str, msg_kan)
        
        r = requests.get(reader_url, timeout=60)
        if r.status_code != 200:
            need_alarm = True
            if msg:
                msg = '%s; [%s]%s' % (msg, now_str, msg_reader)
            else:
                msg = '[%s]%s' % (now_str, msg_reader)
    except Exception, e:
        now = datetime.datetime.now()
        c.logger.error('%s %s' % (str(datetime.datetime.strftime(now, '%Y-%m-%d %H:%M:%S')), str(e)))
        need_alarm = True
        msg = '[%s]%s' % (now_str, msg_exception)
    if need_alarm:
        s = c.redis_instance.incr(c.web_alarm_key)
        if s <= MAX_ALARM_COUNT:
            sms(mobile_list=c.mobile_list, message_post=msg)
        c.logger.error('%s %s' % (str(datetime.datetime.strftime(now, '%Y-%m-%d %H:%M:%S')), msg))
        
if __name__ == '__main__':
    nginx_tcp_check_job()
#    
#    start_time = datetime.datetime.now() - datetime.timedelta(minutes=36) 
#    read_failure_data = AppAvailableData.objects.filter(name='read', result=False, time__gte=start_time).values('time')
#    failure_count = len(read_failure_data)
#    
#    if failure_count >= c.read_alarm_time: 
#        try:
#            start_time = read_failure_data[0]['time']
#            end_time = read_failure_data[failure_count - 1]['time']
#            type = 'read_bookmark'
#            time = get_date_and_time()[1]
#            msg = 'read failure count:%s,%s' % (str(failure_count), time)
#            sms(mobile_list=c.mobile_list, message_post=msg)
#
#            # 获取上一次的报警信息
#            latest = SysAlarm.objects.filter(type=type).order_by('-gmt_create')
#            if latest:
#                latest = latest[0]
#                # start_time是本次报警的开始时间
#                # latest.end_time是上次报警的结束时间
#                # 所有在算时间差的时候, start_time应该是时间差的end, latest.end_time应该是时间差的start
#                tdiff = timediff(latest.end_time, start_time)
#                if (not latest) or start_time > latest.end_time and tdiff > 600:
#                    # 一次新的故障
#                    alarm = SysAlarm(type=type, start_time=start_time, end_time=end_time)
#                    alarm.save()
#                else:
#                    # 添加-报警的定时任务是每10min执行一次, 如果本次报警的时间和上次开始的时间<10min, 则认为是同一次故障
#                    # 同一次故障的持续报警, 只需修改上次的结束时间即可
#                    latest.end_time = end_time
#                    latest.save()
#            else:
#                # 以前没有过这样类型的故障
#                alarm = SysAlarm(type=type, start_time=start_time, end_time=end_time)
#                alarm.save()
#        except Exception, e:
#            c.logger.error(e)
