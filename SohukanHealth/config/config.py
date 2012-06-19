# -*- coding: utf-8 -*-
'''
Created on Jun 18, 2012

@author: liubida
'''
import MySQLdb
import logging
import os

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
    
    cookie = ["Cookie", "access_token = 0381d220305f5acc8dab9a2ab9692a9d09be5e1d"]
    
    add_time_limit = 15
    read_time_limit = 20
    
    '''read worker'''
    bucket_name = 'sohukan'
    expires_seconds = 300


class DevConfig(Config):
    cookie = ["Cookie", "access_token = 0381d220305f5acc8dab9a2ab9692a9d09be5e1d"]
    db_config = {'host':'10.10.58.17', 'port':3306, 'user':'sohupocketlib', 'passwd':'SejJGGk2', 'db':'sohupocketlib'}
    
    logger = logging.getLogger()
    
    @staticmethod
    def do():
        DevConfig.conn = MySQLdb.connect(**DevConfig.db_config)

        handler = logging.FileHandler('../../sohukan.log')
        DevConfig.logger.addHandler(handler)
        DevConfig.logger.setLevel(logging.NOTSET)
        
    
class ProdConfig(Config):
    cookie = ["Cookie", "access_token = eeeb8e686a2a148de62b2352ea88b9c6d4b8bd24"]
    db_config = {'host':'10.10.58.16', 'port':3306, 'user':'sohupocketlib', 'passwd':'SejJGGk2', 'db':'sohupocketlib'}

    logger = logging.getLogger()

    @staticmethod
    def do():
        ProdConfig.conn = MySQLdb.connect(**ProdConfig.db_config)

        handler = logging.FileHandler('../../sohukan.log')
        ProdConfig.logger.addHandler(handler)
        ProdConfig.logger.setLevel(logging.NOTSET)
        
class QaConfig(Config):
    pass

class ConfigFactory:
    
    DEV = DevConfig();
    PROD = ProdConfig();
    QA = QaConfig();
    
    '''这个办法产用Configuration对象。目前而言针对开发，测试，和产品环境，只需要修改返回的值就可以 
    之后可以考虑用不同的方法来适配不同的开发环境'''
    @staticmethod
    def getConfig():
        config = ConfigFactory.DEV
        config.do() 
        return config


c = ConfigFactory().getConfig()

if __name__ == '__main__':
    c = ConfigFactory()
    d = c.getConfig()
    print d.conn
    print d.db_config['host']
