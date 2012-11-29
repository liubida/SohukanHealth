# -*- coding: utf-8 -*-
'''
Created on Jun 18, 2012

@author: liubida
'''
import logging
import os
import redis

class Config:
    ROOT_PATH = os.path.dirname(os.path.dirname(__file__))

    # liubida610@sohu.com
    #["Cookie", "access_token = eeeb8e686a2a148de62b2352ea88b9c6d4b8bd24"],
    # kantest9001@sohu.com
    #["Cookie", "access_token = 0381d220305f5acc8dab9a2ab9692a9d09be5e1d"],
    # fangmeng
    #["Cookie", "access_token = 6662e52138425b995fb6f22b6e6256a3a16d6d89"],
    #["Cookie", "access_token = 80f0630f6a410b559155dd8b87223be1976d558f"],
    #["Cookie", "access_token = 432925e688a245092439b1532408cbccc5dc5e67"]
    
    
    # phone num:
    # liubida 13476852610
    # fangmeng 18627839148
    # fangmeng_tmp 18971149285
    # chenwei 13545257885
    # zhangheng 13437104382'
    
    # log文件的位置
    log_file = ROOT_PATH + '/sohukan.log' 
    report_version = 0

    # 页面红色值
    red = '#c00'
    # 页面绿色值
    green = '#008000'
    # 能看监控页面的用户名
    monitor_user = ['supersohukan', ]
    
    # request查询的最小时间
    MIN_TIME = '2012-01-01 00:00:00'
    # request查询的最大时间
    MAX_TIME = '2222-06-10 00:00:00'
    #  share_channel查询的最小时间, 因为这个功能10-24才上线
    SHARE_CHANNEL_MIN_TIME = '2012-10-24 13:50:00'
    #  share_channel查询的最大时间
    SHARE_CHANNEL_MAX_TIME = MAX_TIME
    # 监控: 添加文章时限
    add_time_limit = 120
    # 报警: 添加文章失败次数上限
    add_alarm_time = 2
    # 监控: 阅读文章时限
    read_time_limit = 100
    # 报警: 阅读文章失败次数上限
    read_alarm_time = 2
    
    bucket_name = 'sohukan'
    expires_seconds = 300
    
    # sys_alarm表中type为'read_bookmar'和'add_bookmark'的为内部原因导致的系统不可用
    self_alarm_type = ['read_bookmark', 'add_bookmark']
    
    color = ['#FF0F00', '#FF9E01', '#FCD202', '#F8FF01', '#B0DE09', '#04D215',
             '#0D8ECF', '#0D52D1', '#2A0CD0', '#8A0CCF', '#CD0D74']

    test_id = [2, 3, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 22, 23, 24, 25, 29,
               32, 33, 35, 43, 46, 53, 58, 91, 108, 125, 165, 591, 1288, 1486, 2412, 3373]

    # 测试账户的access_token
    # cookie = ["Cookie", "access_token = 0381d220305f5acc8dab9a2ab9692a9d09be5e1d"]
    cookie = ["Cookie", "access_token = eeeb8e686a2a148de62b2352ea88b9c6d4b8bd24"]

    db_config = {'host':'10.10.58.17', 'port':3306, 'user':'sohupocketlib', 'passwd':'SejJGGk2', 'db':'sohupocketlib'}
    db_self_config = {'host':'10.10.69.53', 'port':3306, 'user':'sohukan', 'passwd':'sohukan', 'db':'sohukanhealth'}
    redis_config = {'host':'10.10.69.53', 'port':6379, 'db':4}
    redis_instance = redis.StrictRedis(**redis_config)
    logger = logging.getLogger("SohukanHealth")
    
    def do(self):
        handler = logging.FileHandler(self.log_file)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.ERROR)
    
class DevConfig(Config):
    mobile_list = '13476852610'
    ha_nginx_check_url = 'http://10.11.6.175/status'
    
class ProdConfig(Config):
    mobile_list = '13476852610,18627839148,13545257885,13437104382,18971149285'
    ha_nginx_check_url = 'http://../status'

class ConfigFactory:
    
    '''这个办法产用Configuration对象。目前而言针对开发，测试，和产品环境，只需要修改返回的值就可以 
    之后可以考虑用不同的方法来适配不同的开发环境'''
    def getConfig(self):
        import socket
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        
        if ip in ('10.10.69.53'):
            ENV_TAG = 'prod'
        elif ip in ('10.7.8.58'):
            ENV_TAG = 'dev'
        else:
            ENV_TAG = None
        
        if ENV_TAG == 'prod':
            config = ProdConfig();
        elif ENV_TAG == 'dev':
            config = DevConfig();
            pass
        else:
            return None
        
        config.do() 
        return config

c = ConfigFactory().getConfig()
#lock = threading.Lock()

if __name__ == '__main__':
#    c = ConfigFactory()
#    d = c.getConfig()
#    print d.conn
#    print d.db_config['host']
    print 'supersohukan' in c.monitor_user
#    a = os.path.dirname(__file__)
#    print a
#    b = os.path.dirname(a)
#    print b
