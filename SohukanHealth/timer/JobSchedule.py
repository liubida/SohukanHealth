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

from monitor.system.job import add_job, read_job, user_total_job, \
    bookmark_total_job, add_and_read_alarm_job

#class Sched(object):
#    def __init__(self):
#        "disable the __init__ method"
#    
#    __instance = None
#    __lock = threading.Lock()
#    
#    @staticmethod
#    def get_instance():
#        Sched.__lock.acquire()
#        if not Sched.__instance:
#            Sched.__instance = Scheduler(daemonic=True)
#            object.__init__(Sched.__instance)
#        Sched.__lock.release()
#        return Sched.__instance
#    
#def status(sched):        
#    try:
#        return sched.running
#    except Exception, e:
#        print e
#        return False
#    


#def start_job():
#    try:
#        sched = Sched.get_instance()
#        print sched
#        sched_status = status(sched)
#        print sched_status
#        
#        if not sched_status:
#    #        add_job = sched.add_cron_job(add_job, second='*/1')
#    #        read_job = sched.add_cron_job(read_job, second='*/10')
#    #        usertotal_job = sched.add_cron_job(user_total_job, second='*/20')
#    #        bookmarktotal_job = sched.add_cron_job(bookmark_total_job, second='*/15')
#            sched.add_cron_job(add_job, minute='*/5')
#            sched.add_cron_job(read_job, minute='*/5')
#            sched.add_cron_job(add_and_read_alarm_job, minute='*/10')
#            sched.add_cron_job(user_total_job, minute='*/60')
#            sched.add_cron_job(bookmark_total_job, minute='*/60')
#            sched.start()
#            return 'job start'
#        else:
#            return 'job started already'
#    except Exception, e:
#        c.logger.error(e)
#        return str(e)
#    finally:
#        pass


if __name__ == '__main__':
    if len(sys.argv) != 2:
        pass
    else:
        method_name = sys.argv[1]
        if method_name == 'add_job': add_job()
        elif method_name == 'read_job': read_job()
        elif method_name == 'add_and_read_alarm_job': add_and_read_alarm_job()
        elif method_name == 'user_total_job': user_total_job()
        elif method_name == 'bookmark_total_job': bookmark_total_job()
        else: pass

#  */5  *  *  *  *   sohukan  python /home/sohukan/SohukanHealth/SohukanHealth/timer/JobSchedule.py add_job
#  */5  *  *  *  *   sohukan  python /home/sohukan/SohukanHealth/SohukanHealth/timer/JobSchedule.py read_job
#  */10 *  *  *  *   sohukan  python /home/sohukan/SohukanHealth/SohukanHealth/timer/JobSchedule.py add_and_read_alarm_job
#   *  */1  *  *  *   sohukan  python /home/sohukan/SohukanHealth/SohukanHealth/timer/JobSchedule.py user_total_job
#   *  */1  *  *  *   sohukan  python /home/sohukan/SohukanHealth/SohukanHealth/timer/JobSchedule.py bookmark_total_job