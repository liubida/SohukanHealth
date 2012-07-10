# -*- coding: utf-8 -*-
'''
Created on Jul 10, 2012

@author: liubida
'''
import logging
import syslog


class SyslogHandler(logging.Handler, object):
    def __init__(self):
        logging.Handler.__init__(self)

    def emit(self, record):
        r = str(record)
        print 'syslog:', r
        
        self.format(record)
        try:
            syslog.openlog('',syslog.LOG_PID, syslog.LOG_LOCAL2)
            syslog.syslog(record.message)
        except Exception, e:
            syslog.openlog('',syslog.LOG_PID, syslog.LOG_LOCAL2)
            syslog.syslog(str(e))
