# -*- coding: utf-8 -*-
'''
Created on Jun 13, 2012

@author: liubida
'''

import sys
import os
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)
from django.core.management import setup_environ
from SohukanHealth import settings
setup_environ(settings)

from job import add_job, read_job, user_total_job, \
    bookmark_total_job, add_alarm_job, read_alarm_job, day_report_job, week_report_job, fix_ua_job, \
    rabbitmq_queue_alarm_job, day_aggregation_job
from alarm_job import nginx_tcp_check_job, web_alarm_job


if __name__ == '__main__':
    if len(sys.argv) != 2:
        pass
    else:
        method_name = sys.argv[1]
        if method_name == 'add_job': add_job()
        elif method_name == 'read_job': read_job()
        elif method_name == 'add_alarm_job': add_alarm_job()
        elif method_name == 'read_alarm_job': read_alarm_job()
        elif method_name == 'user_total_job': user_total_job()
        elif method_name == 'bookmark_total_job': bookmark_total_job()
        elif method_name == 'shorturl_total_job': shorturl_total_job()
        elif method_name == 'day_report_job': day_report_job()
        elif method_name == 'week_report_job': week_report_job()
        elif method_name == 'fix_ua_job' : fix_ua_job()
        elif method_name == 'rabbitmq_queue_alarm_job' : rabbitmq_queue_alarm_job()
        elif method_name == 'day_aggregation_job' : day_aggregation_job()
        elif method_name == 'web_alarm_job' : web_alarm_job()
        #elif method_name == 'nginx_tcp_check_job' : nginx_tcp_check_job()
        
        else: pass

# */5  *    *  *  *   sohukan  python /home/sohukan/SohukanHealth/SohukanHealth/timer/JobSchedule.py add_job
# */5  *    *  *  *   sohukan  python /home/sohukan/SohukanHealth/SohukanHealth/timer/JobSchedule.py read_job
# */5  *    *  *  *   sohukan  python /home/sohukan/SohukanHealth/SohukanHealth/timer/JobSchedule.py add_alarm_job
# */5  *    *  *  *   sohukan  python /home/sohukan/SohukanHealth/SohukanHealth/timer/JobSchedule.py read_alarm_job
# 5    */1  *  *  *   sohukan  python /home/sohukan/SohukanHealth/SohukanHealth/timer/JobSchedule.py user_total_job
# 10   */1  *  *  *   sohukan  python /home/sohukan/SohukanHealth/SohukanHealth/timer/JobSchedule.py bookmark_total_job
# 58   23   *  *  *   sohukan  python /home/sohukan/SohukanHealth/SohukanHealth/timer/JobSchedule.py day_report_job
# 50   6    *  *  *   sohukan  python /home/sohukan/SohukanHealth/SohukanHealth/timer/JobSchedule.py week_report_job
# 15   */3  *  *  *   sohukan  python /home/sohukan/SohukanHealth/SohukanHealth/timer/JobSchedule.py fix_ua_job
# */14 *    *  *  *   sohukan  python /home/sohukan/SohukanHealth/SohukanHealth/timer/JobSchedule.py rabbitmq_queue_alarm_job
# 52   23   *  *  *   sohukan  python /home/sohukan/SohukanHealth/SohukanHealth/timer/JobSchedule.py day_aggregation_job
# */3  *    *  *  *   sohukan  python /home/sohukan/SohukanHealth/SohukanHealth/timer/JobSchedule.py nginx_tcp_check_job
# */3  *    *  *  *   sohukan  python /home/sohukan/SohukanHealth/SohukanHealth/timer/JobSchedule.py web_alarm_job

