# Create your views here.

'''
Created on May 19, 2013

@author: cescgao
'''

from config.config import c
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
import MySQLdb

@login_required
def feedback(request):
    try:
        conn = MySQLdb.connect(**c.db_prod_config)
        cur = conn.cursor()
        sql = 'select * from feedback_feedback;'
        cur.execute(sql)
        results = cur.fetchall()
    except Exception, e:
        c.logger.error(e)
    finally:
        try:
            cur.close()
        except Exception, e:
            c.logger.error(e)
        finally:
            if conn:
                conn.close()
    rtn = []
    for d in results:
        rtn.append({
                'id': d[0],
                'email': d[1],
                'content': d[2],
                'user_id': d[3],
                'gmt_create': d[4].strftime('%Y-%M-%d %H:%m:%S') if d[4] else '',
                'gmt_modify': d[5], 
                'os': d[6],
                'version': d[7],
                'device_model': d[8]
                })
    rtn = sorted(rtn, key = lambda x: x['id'], reverse = True)
    return render_to_response('internal/feedback.html', locals())
