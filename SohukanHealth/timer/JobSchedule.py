'''
Created on Jun 13, 2012

@author: liubida
'''

import sys
sys.path.append('/home/liubida/git/SohukanHealth/SohukanHealth/')
print sys.path

from django.core.management import setup_environ
from SohukanHealth import settings
print settings
setup_environ(settings)

from apscheduler.scheduler import Scheduler
from monitor.system.job import add_job, read_job, user_total_job, bookmark_total_job
from config.config import c

if __name__ == '__main__':
    try:
        sched = Scheduler(daemonic=False)
        
        add_job = sched.add_cron_job(add_job, minute='*/5')
        read_job = sched.add_cron_job(read_job, minute='*/2')
        usertotal_job = sched.add_cron_job(user_total_job, minute='*/20')
        bookmarktotal_job = sched.add_cron_job(bookmark_total_job, minute='*/15')
        #s3job = sched.add_cron_job(print_1, second='*/10')
        sched.start()
    except Exception as e:
        print e
    finally:
        if c.conn:
            c.conn.close()
