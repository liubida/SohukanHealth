# -*- coding: utf-8 -*-
'''
Created on Jun 13, 2012

@author: liubida
'''

import sys
import os
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print root_path
sys.path.append(root_path)
print sys.path

from django.core.management import setup_environ
from SohukanHealth import settings
print settings
setup_environ(settings)

from job import add_job, read_job, user_total_job, \
    bookmark_total_job, add_alarm_job, read_alarm_job, day_report_job,fix_ua_job


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
        elif method_name == 'day_report_job': day_report_job()
        elif method_name == 'fix_ua_job' : fix_ua_job()
        else: pass

# */5  *    *  *  *   sohukan  python /home/sohukan/SohukanHealth/SohukanHealth/timer/JobSchedule.py add_job
# */5  *    *  *  *   sohukan  python /home/sohukan/SohukanHealth/SohukanHealth/timer/JobSchedule.py read_job
# */10 *    *  *  *   sohukan  python /home/sohukan/SohukanHealth/SohukanHealth/timer/JobSchedule.py add_alarm_job
# */10 *    *  *  *   sohukan  python /home/sohukan/SohukanHealth/SohukanHealth/timer/JobSchedule.py read_alarm_job
# 5    */1  *  *  *   sohukan  python /home/sohukan/SohukanHealth/SohukanHealth/timer/JobSchedule.py user_total_job
# 10   */1  *  *  *   sohukan  python /home/sohukan/SohukanHealth/SohukanHealth/timer/JobSchedule.py bookmark_total_job
# 58   23   *  *  *   sohukan  python /home/sohukan/SohukanHealth/SohukanHealth/timer/JobSchedule.py day_report_job
# 15   */5  *  *  *   sohukan  python /home/sohukan/SohukanHealth/SohukanHealth/timer/JobSchedule.py fix_ua_job
