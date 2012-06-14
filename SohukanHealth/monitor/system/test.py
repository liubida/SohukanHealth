# -*- coding: utf-8 -*-
'''
Created on Jun 7, 2012

@author: liubida
'''

from monitor.system.worker import add_worker, read_worker
from util import get_date_and_time
from util.random_spider import RandomSpider
import json
import logging
import os

# liubida610@sohu.com
#["Cookie", "access_token = eeeb8e686a2a148de62b2352ea88b9c6d4b8bd24"],
# kantest9001@sohu.com
#["Cookie", "access_token = 0381d220305f5acc8dab9a2ab9692a9d09be5e1d"],
# fangmeng
#["Cookie", "access_token = 6662e52138425b995fb6f22b6e6256a3a16d6d89"],
#["Cookie", "access_token = 80f0630f6a410b559155dd8b87223be1976d558f"],
#["Cookie", "access_token = 432925e688a245092439b1532408cbccc5dc5e67"]

cookie = ["Cookie", "access_token = 0381d220305f5acc8dab9a2ab9692a9d09be5e1d"]

file_name = os.path.join(os.path.dirname(__file__), 'test.data.js').replace('\\', '/')

class LogData():
    def __init__(self, file_name=None):
        if not file_name:
            logging.error("logData init error: file_name should not be None")
            return
        self.file_name = file_name
        self.date, self.time = get_date_and_time()
        self.log_data = self._read_from_file()
        self._set_today_data()
        
    def _set_today_data(self):
        if self._is_new_day():
            # if it's a new day
            o = {}
            o['date'] = self.date
            o['read_count'] = 0
            o['read_success'] = 0
            o['add_count'] = 0
            o['add_success'] = 0
            o['info'] = []
            self.today_data = o
            self.log_data.append(self.today_data)
        else:
            self.today_data = self.log_data[-1]

    def _read_from_file(self):
        f = None
        try:
            f = open(self.file_name, 'r')
            obj = json.load(f)
            # 按date正序排列
            obj.sort(key=lambda x:x['date'])
        except Exception as e:
            logging.error("read_from_file error: ", e)
            return []
        else:
            return obj
        finally:
            if f:
                f.close()
                
    def _is_new_day(self):
        if not len(self.log_data):
            return True
        else:
            if self.log_data[-1]['date'] == self.date:
                return False
            else:
                return True
    
    def append_today_date(self, read_value, add_value):
        '''
        read_value={"time_used" : 4,"result" : True}
        add_value ={"time_used" : 4,"result" : False}
        '''
        o = {}
        o['time'] = self.time
        o['read'] = read_value
        o['add'] = add_value
        
        self.log_data[-1]['read_count'] += 1
        self.log_data[-1]['add_count'] += 1
        
        if read_value['result']:
            self.log_data[-1]['read_success'] += 1
        if add_value['result']:
            self.log_data[-1]['add_success'] += 1
            
        self.today_data['info'].append(o)
    
    def write_to_file(self):
        f = None
        try:
            f = open(self.file_name, 'w')
            json.dump(self.log_data, f, separators=(',', ':'))
        except Exception as e:
            logging.error("write_to_file error: ", e)
        finally:
            if f:
                f.close()
    
    def get_data_by_date(self, date):
        if not len(self.log_data):
            return None

        for d in self.log_data:
            if d['date'] == date:
                return d
        
        return None
    
if __name__ == '__main__':
    url = RandomSpider().get_valid_url()
        
    log_data = LogData(file_name)
    
    add = add_worker(url, cookie)
    add_value = add.test()
    
    read = read_worker(cookie)
    read_value = read.test()
    
    log_data.append_today_date(read_value, add_value)
    log_data.write_to_file()
