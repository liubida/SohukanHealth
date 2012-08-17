# -*- coding: utf-8 -*-
'''
Created on Jul 5, 2012

@author: liubida
'''
from config.config import c
import urllib

def sms(mobile_list=None, message_post=None):
    if None == mobile_list or None == message_post:
        return False
    url = 'http://mtpc.sohu.com/smsnotify'
    p = {}
    p['message_post'] = message_post.encode('gbk')
    p['mobile_list'] = mobile_list
    try:
        urllib.urlopen(url, urllib.urlencode(p))
        c.logger.info(str(p))
        return True
    except Exception, e :
        c.logger.error(e)
        return False

#This code is for debugging and unit testing    
if __name__ == '__main__':
    sms('13476852610,13545257885', 'test by sohukanhealth')
