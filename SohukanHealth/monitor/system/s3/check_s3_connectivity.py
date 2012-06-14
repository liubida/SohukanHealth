'''
Created on Jun 14, 2012

@author: liubida
'''

from exception import JobException
import mod_storage_helper
import time
import urllib2

def check_s3():
    status = True
    url = mod_storage_helper.get_expire_data_url('sohukan', 'bookmark-prod-24-1274', 60)
    try:
        mod_storage_helper.store_data_from_string('sohukan', 'bookmark-prod-24-1274', 'foo')
    except Exception, exc:
        raise JobException(exc)
        status = False
    try:
        urllib2.urlopen(url)
    except Exception, exc:
        raise JobException(exc)
        status = False
    
    return status

if __name__ == '__main__':
    
    def infinite_check():
        counter = 0
        while True:
            print '[counter %s]' % counter,
            check_s3()
            print
            time.sleep(10)
            counter += 1

    infinite_check()
