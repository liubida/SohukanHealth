# -*- coding: utf-8 -*-
#
# by cescgao
# 2013-3-21
# 
# sohukanhealth数据库太大，查询不便，使用此脚本按时间导出
# 使用anyjson以字典形式写入，以换行符分隔

from config.config import c
import MySQLdb
import datetime
import sys, os
import anyjson

FILE_SIZE = 10000

def process(date):
    index = 0
    if not os.path.exists('mysql'):
        os.mkdir('mysql')
    time = 2
    try:
        conn = MySQLdb.connect(**c.db_self_config)
        cursor = conn.cursor()
        while(time > 0):
            sql = "select * from stats_operobject where gmt_create < %s limit %s" % (FILE_SIZE, date)
            cursor.execute(sql)
            results = cursor.fetchall()
            if len(results) == 0:
                break
            index += 1
            content = ''
            for r in results:
                dic = {"id": "%s" % r[0], "user_id": "%s" % r[1], "oper_id": "%s" % r[2], "object_type": r[3], "object_key": r[4], "gmt_create": r[5].strftime("%Y-%m-%d"), "gmt_modify": r[6].strftime("%Y-%m-%d")}
                content += anyjson.dumps(dic) + '\n'
            w = open('mysql/operobject_%s_%s.txt' % (datetime.datetime.strftime(date, '%Y-%m-%d'), index), 'w')
            w.writelines(content)
            w.close()
            sql = "delete from stats_operobject where id <= %s" % r[0]
            cursor.execute(sql)
            conn.commit()
            if len(results) < FILE_SIZE:
                break
            time -= 1
    except Exception, e:
        print e
    finally:
        try:
            if cursor:
                cursor.close()
        except Exception, e:
            print e
        finally:
            if conn:
                conn.close()

if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print "Usage: need a datetime '%Y-%m-%d'"
    else:
        date = datetime.datetime.strptime(sys.argv[1], '%Y-%m-%d')
        process(date)
