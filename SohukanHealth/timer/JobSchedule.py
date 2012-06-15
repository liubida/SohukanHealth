'''
Created on Jun 13, 2012

@author: liubida
'''

from apscheduler.scheduler import Scheduler
from monitor.system.job import read_job, add_job, user_total_job

sched = Scheduler(daemonic=False)

add_job = sched.add_cron_job(add_job, minute='*/5')
read_job = sched.add_cron_job(read_job, minute='*/2')
usertotal_job = sched.add_cron_job(user_total_job, minute='*/10')
#s3job = sched.add_cron_job(print_1, second='*/10')
sched.start()
