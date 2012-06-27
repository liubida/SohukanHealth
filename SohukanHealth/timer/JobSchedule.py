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

from config.config import c
from apscheduler.scheduler import Scheduler
from monitor.system.job import add_job, read_job, user_total_job, \
    bookmark_total_job

if __name__ == '__main__':
    try:    
        sched = Scheduler(daemonic=False)
#        add_job = sched.add_cron_job(add_job, second='*/1')
#        read_job = sched.add_cron_job(read_job, second='*/10')
#        usertotal_job = sched.add_cron_job(user_total_job, second='*/20')
#        bookmarktotal_job = sched.add_cron_job(bookmark_total_job, second='*/15')
        addjob = sched.add_cron_job(add_job, minute='*/10')
        readjob = sched.add_cron_job(read_job, minute='*/15')
        usertotaljob = sched.add_cron_job(user_total_job, minute='*/60')
        bookmarktotaljob = sched.add_cron_job(bookmark_total_job, minute='*/60')
        sched.start()
    except Exception, e:
        c.logger.error(e)
    finally:
        pass
