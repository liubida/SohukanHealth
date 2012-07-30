# -*- coding: utf-8 -*-
'''
Created on Jun 14, 2012

@author: liubida
'''
from config.config import c
from exception import MonitorException
from lxml import etree
from monitor.system.s3.mod_storage_helper import get_expire_data_url
from util import mytimer, request
from util.random_spider import RandomSpider
import datetime
import threading
import time
import urllib

class login_worker():
    def __init__(self, cookie=None):
        self.cookie = cookie

class add_worker():
    def __init__(self, url=None, cookie=None):
        if None == cookie:
            raise MonitorException('cookie should not be None')
        if None == url:
            raise MonitorException('url should not be None')

        self.url = url
        self.cookie = cookie
        self.result = False
        self.flag = True
        self.event = threading.Event()
    
    def test(self):
        try:
            time_used = self.add()
        except Exception, e:
            c.logger.error(e)
            ret = {"result" : False, "time_used" : c.add_time_limit, 'comments': str(e)}
        else:
            ret = {"result" : True, "time_used" : time_used}
        finally:
            return ret            
    
    @mytimer
    def add(self):
        self._add_bookmark()
        expire_time = datetime.datetime.now() + datetime.timedelta(seconds=c.add_time_limit)
        add_result = self._check_bookmark(self.url, self.cookie)

        if expire_time < datetime.datetime.now():
            raise MonitorException('add_bookmark_timeout, url:%s' % self.url)
        
        if not add_result:
            raise MonitorException('add_bookmark_error, url:%s' % self.url)
            
    def _check_bookmark(self, check_url, cookie):
        url_bookmarks_list = "http://kan.sohu.com/api/2/bookmarks/list/";
        data = urllib.urlencode({"order_by":"-create_time", "limit":1, "submit":"提交"});
        try:
            response = request(url_bookmarks_list, data, cookie);
            s = response.read()
            
            node = etree.fromstring(s, parser=etree.XMLParser(remove_blank_text=True))
            bookmark = node.find('bookmark')
            bookmark_url = bookmark.findtext('url')
            return bookmark_url == check_url
        except Exception, e:
            c.logger.error(e)
            return False
    
    def _add_bookmark(self):
        url_add = "http://kan.sohu.com/api/2/bookmarks/add/"
        
        data = urllib.urlencode({"url":self.url, "submit":"提交"});
        response = request(url_add, data, self.cookie);
        
        if 200 != response.code:
            raise MonitorException('add_bookmark_error, url:%s' % str(self.url))
            
class read_worker():
    # TODO: change to the single instance
    def __init__(self, cookie=None):
        if None == cookie:
            raise MonitorException('cookie should not be None')

        self.cookie = cookie
        
    def test(self):
        try:
            time_used = self.read()
        except Exception, e:
            c.logger.error(e)
            ret = {"result" : False, "time_used" : c.read_time_limit, 'comments': str(e)}
        else:
            ret = {"result" : True, "time_used" : time_used}
        finally:
            return ret       
        
    @mytimer
    def read(self):
        expire_time = datetime.datetime.now() + datetime.timedelta(seconds=c.read_time_limit)
        bookmark_id = self._get_bookmark_id()
        self._get_text(bookmark_id)
        self._get_resource(bookmark_id)

        if expire_time < datetime.datetime.now():
            raise MonitorException('read_bookmark_timeout')
    
    def _get_bookmark_id(self):
        '''
        get the lastest bookmark_id and bookmark_url
        '''
        url_bookmarks_list = "http://kan.sohu.com/api/2/bookmarks/list/";
        data = urllib.urlencode({"order_by":"-create_time", "limit":1, "submit":"提交"});
        response = request(url_bookmarks_list, data, self.cookie);
        s = response.read()
        
        node = etree.fromstring(s, parser=etree.XMLParser(remove_blank_text=True))
        bookmark = node.find('bookmark')
        bookmark_id = bookmark.get('id')
        
        return bookmark_id
    
    def _get_text(self, bookmark_id=None):
        '''
        get the text by bookmark_id
        '''
        if None == bookmark_id:
            raise MonitorException('bookmark_id is None')
        
        url_bookmarks_get_text = "http://kan.sohu.com/api/2/bookmarks/get-text/";
        
        data = urllib.urlencode({"bookmark_id":bookmark_id, "submit":"提交"});
        response = request(url_bookmarks_get_text, data, self.cookie);
        if 200 != response.code:
            raise MonitorException('get_text_error, bookmark_id:%s' % str(bookmark_id))
        
    def _get_resource(self, bookmark_id=None):
        '''
        get the resource by bookmark_id
        '''
        if None == bookmark_id:
            raise MonitorException('get_reousrce_error, bookmark_id is None')
        
        url_bookmarks_get_resource = "http://kan.sohu.com/api/2/bookmarks/get-resource/";

        data = urllib.urlencode({"bookmark_id":bookmark_id, "submit":"提交"});
        response = request(url_bookmarks_get_resource, data, self.cookie);
        if 200 == response.code:
            node = etree.fromstring(response.read(), parser=etree.XMLParser(remove_blank_text=True))
            images = node.findall("image")
            if images:
                for i in images:
                    key = i.get("key", None)
                    self._get_img_1(key)
                    self._get_img_2(key)
        else:
            raise MonitorException('get_resource_error, bookmark_id:%s' % str(bookmark_id))
        
    def _get_img_1(self, key=None):
        '''
        get the image by resource key with sohukan
        '''
        if None == key:
            raise MonitorException('get_image_1_error, key is None') 
            
        url_bookmarks_get_raw = "http://kan.sohu.com/api/2/resources/image/get-raw/";
        data = urllib.urlencode({"key":key, "submit":"提交"});
        response = request(url_bookmarks_get_raw, data, self.cookie);
        if 200 != response.code:
            raise MonitorException('get_image_1_error, key:%s' % key)
        
    def _get_img_2(self, key=None):
        '''
        get the image by resource key with s3 direct
        '''
        if None == key:
            raise MonitorException('get_image_2_error, key is None') 
        url_bookmarks_get_raw_s3 = get_expire_data_url(c.bucket_name, key, c.expires_seconds)
        response = request(url_bookmarks_get_raw_s3);
        if 200 != response.code:
            raise MonitorException('get_image_2_error, url:%s, response.code:%d' % (url_bookmarks_get_raw_s3, response.code))

if __name__ == '__main__':
    cookie = ["Cookie", "access_token = eeeb8e686a2a148de62b2352ea88b9c6d4b8bd24"]
    for i in range(20):
        url = RandomSpider().get_valid_url()
        print url
        a = add_worker(url, cookie)
        try:
            a.test()
            time.sleep(4)
        except Exception, e:
            print e
        print '...'

#    b = read_worker(cookie)
#    print b.test()
    
