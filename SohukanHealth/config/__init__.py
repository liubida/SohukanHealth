
'''
Created on 2012-5-31

@author: diracfang
'''
import MySQLdb
import datetime
import urllib2

db_config = {'host':'10.10.58.17', 'port':3306, 'user':'sohupocketlib', 'passwd':'SejJGGk2', 'db':'sohupocketlib'}
conn = MySQLdb.connect(**db_config)

class DBHelper():
    def __init__(self):
        pass
    
    
    
#     except MySQLdb.Error, e:
#     print "Error %d: %s" % (e.args[0], e.args[1])
#     sys.exit (1)
#
#cursor = conn.cursor()
#keys = []
#f = open('c:/broken.txt', 'wb')
#for i in range(64):
#    cursor.execute ("select * from bookmark_bookmark_%s" % i)
#    rows = cursor.fetchall()
#    for row in rows:
#        if row[8] >= datetime.datetime(2012, 5, 29):
#            keys.append('bookmark-%s-%s-%s' % ('prod', row[1], row[0]))
#cursor.close()
#conn.close()
#
#print len(keys)
#count = 1
#for key in keys:
#    print count,
#    count += 1
#    url = ''
#    try:
#        resp = urllib2.urlopen(url)
#        data = resp.read()
#    except:
#        print key
#        f.write(key)
#        f.write('\n')
#    else:
#        print 'ok'
#f.close()
