'''
Created on Jun 13, 2012

@author: liubida
'''

from apscheduler.scheduler import Scheduler
from monitor.system.read import monitor_read, monitor_add

sched = Scheduler(daemonic=False)

addjob = sched.add_cron_job(monitor_add, second='*/20')
readjob = sched.add_cron_job(monitor_read, second='*/30')
#s3job = sched.add_cron_job(print_1, second='*/10')
sched.start()
