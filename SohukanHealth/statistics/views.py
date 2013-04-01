# -*- coding: utf-8 -*-
# Create your views here.
from config.config import c
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from django.template.context import Context
from django.views.decorators.http import last_modified
from monitor.models import SomeTotal
from statistics.biz import get_bookmark_per_user, get_bookmark_time, \
    get_bookmark_percent, get_data_interval, add_inc_for_data, get_activate_user, \
    get_bookmark_website, get_user_platform, _get_week_list, \
    get_bookmark_website_for_user, get_bookmark_website_detail, get_conversion
from statistics.biz_comp import get_share_channels, get_public_client
from statistics.models import Report
from util import get_week_num, http_conditions
import anyjson
import datetime

'''综合'''

# 综合页面首页
@login_required
def statistics(request):
    t = loader.get_template('statistics/statistics.html')
    c = Context({
        'user': request.user
    })

    return HttpResponse(t.render(c))

# 综合 注册用户数统计
@login_required
def user_total(request):
    start_time = request.GET.get('start_time', c.MIN_TIME)
    end_time = request.GET.get('end_time', c.MAX_TIME)
    data_grain = request.GET.get('data_grain', 'day')
    data_grain = data_grain if data_grain else 'day'
    
    if start_time == 'NaN-aN-aN aN:aN:aN': 
        start_time = c.MIN_TIME
    if end_time == 'NaN-aN-aN aN:aN:aN': 
        end_time = c.MAX_TIME

    data = {'list':[]}
    raw_data = SomeTotal.objects.filter(name='user', time__gte=start_time, time__lte=end_time).values('time', 'count')
    
    if data_grain == 'hour':
        for d in raw_data:
            data['list'].append({'time':d['time'].strftime('%m-%d %H:%M:%S'), 'count':d['count']})
    elif data_grain == 'day':
        delta = datetime.timedelta(days=1)
        # 每天取一个23点的数据
        data['list'] = get_data_interval(raw_data, delta)
    elif data_grain == 'week':
        # 每隔7天取一个23点的数据
        delta = datetime.timedelta(days=7)
        data['list'] = get_data_interval(raw_data, delta)
    elif data_grain == 'month':
        # 每隔4周天取一个23点的数据
        delta = datetime.timedelta(weeks=4)
        data['list'] = get_data_interval(raw_data, delta)

    # 计算data的增长率
    add_inc_for_data(data)
    
    response = HttpResponse(anyjson.dumps(data))
    # 缓存一天, 也只能缓存一天
    # 因为start_time和end_time可能是NA, 那么一天之后, 这个NA的数据实际上是会发生变化的.
    now = datetime.datetime.now()
    expire = now + datetime.timedelta(days=1)
    response['Expires'] = expire.strftime('%a, %d %b %Y 01:00:00 %Z')
    return response

# 综合 收藏文章数统计
@login_required
def bookmark_total(request):
    start_time = request.GET.get('start_time', c.MIN_TIME)
    end_time = request.GET.get('end_time', c.MAX_TIME)
    data_grain = request.GET.get('data_grain', 'day')
    data_grain = data_grain if data_grain else 'day'
    
    if start_time == 'NaN-aN-aN aN:aN:aN': 
        start_time = c.MIN_TIME
    if end_time == 'NaN-aN-aN aN:aN:aN': 
        end_time = c.MAX_TIME

    data = {'list':[]}
    raw_data = SomeTotal.objects.filter(name='bookmark', time__gte=start_time, time__lte=end_time).values('time', 'count')
    if data_grain == 'hour':
        for d in raw_data:
            data['list'].append({'time':d['time'].strftime('%m-%d %H:%M:%S'), 'count':d['count']})
    elif data_grain == 'day':
        delta = datetime.timedelta(days=1)
        # 每天取一个23点的数据
        data['list'] = get_data_interval(raw_data, delta)
    elif data_grain == 'week':
        # 每隔7天取一个23点的数据
        delta = datetime.timedelta(days=7)
        data['list'] = get_data_interval(raw_data, delta)
    elif data_grain == 'month':
        # 每隔4周天取一个23点的数据
        delta = datetime.timedelta(weeks=4)
        data['list'] = get_data_interval(raw_data, delta)

    # 计算data的增长率
    add_inc_for_data(data)
    
    response = HttpResponse(anyjson.dumps(data))
    # 缓存一天
    now = datetime.datetime.now()
    expire = now + datetime.timedelta(days=1)
    response['Expires'] = expire.strftime('%a, %d %b %Y 01:00:00 %Z')
    return response


# 综合 收藏小说数统计
@login_required
def fiction_total(request):
    start_time = request.GET.get('start_time', c.MIN_TIME)
    end_time = request.GET.get('end_time', c.MAX_TIME)
    data_grain = request.GET.get('data_grain', 'day')
    data_grain = data_grain if data_grain else 'day'
    
    if start_time == 'NaN-aN-aN aN:aN:aN': 
        start_time = c.MIN_TIME
    if end_time == 'NaN-aN-aN aN:aN:aN': 
        end_time = c.MAX_TIME

    data = {'list':[]}
    raw_data = SomeTotal.objects.filter(name='fiction', time__gte=start_time, time__lte=end_time).values('time', 'count')
    if data_grain == 'hour':
        for d in raw_data:
            data['list'].append({'time':d['time'].strftime('%m-%d %H:%M:%S'), 'count':d['count']})
    elif data_grain == 'day':
        delta = datetime.timedelta(days=1)
        # 每天取一个23点的数据
        data['list'] = get_data_interval(raw_data, delta)
    elif data_grain == 'week':
        # 每隔7天取一个23点的数据
        delta = datetime.timedelta(days=7)
        data['list'] = get_data_interval(raw_data, delta)
    elif data_grain == 'month':
        # 每隔4周天取一个23点的数据
        delta = datetime.timedelta(weeks=4)
        data['list'] = get_data_interval(raw_data, delta)

    # 计算data的增长率
    add_inc_for_data(data)
    
    response = HttpResponse(anyjson.dumps(data))
    # 缓存一天
    now = datetime.datetime.now()
    expire = now + datetime.timedelta(days=1)
    response['Expires'] = expire.strftime('%a, %d %b %Y 01:00:00 %Z')
    return response


# 综合 邮件收藏文章数统计
@login_required
def bookmark_email(request):
    start_time = request.GET.get('start_time', c.MIN_TIME)
    end_time = request.GET.get('end_time', c.MAX_TIME)
    data_grain = request.GET.get('data_grain', 'day')
    data_grain = data_grain if data_grain else 'day'
    
    if start_time == 'NaN-aN-aN aN:aN:aN': 
        start_time = c.MIN_TIME
    if end_time == 'NaN-aN-aN aN:aN:aN': 
        end_time = c.MAX_TIME

    data = {'list':[]}
    raw_data = SomeTotal.objects.filter(name='email', time__gte=start_time, time__lte=end_time).values('time', 'count')
    if data_grain == 'hour':
        for d in raw_data:
            data['list'].append({'time':d['time'].strftime('%m-%d %H:%M:%S'), 'count':d['count']})
    elif data_grain == 'day':
        delta = datetime.timedelta(days=1)
        # 每天取一个23点的数据
        data['list'] = get_data_interval(raw_data, delta)
    elif data_grain == 'week':
        # 每隔7天取一个23点的数据
        delta = datetime.timedelta(days=7)
        data['list'] = get_data_interval(raw_data, delta)
    elif data_grain == 'month':
        # 每隔4周天取一个23点的数据
        delta = datetime.timedelta(weeks=4)
        data['list'] = get_data_interval(raw_data, delta)

    # 计算data的增长率
    add_inc_for_data(data)
    
    response = HttpResponse(anyjson.dumps(data))
    # 缓存一天
    now = datetime.datetime.now()
    expire = now + datetime.timedelta(days=1)
    response['Expires'] = expire.strftime('%a, %d %b %Y 01:00:00 %Z')
    return response


# 综合 分享渠道统计
@login_required
#@last_modified(http_conditions.share_channels_last_modified)
def share_channels(request):
    start_time = request.GET.get('start_time', c.SHARE_CHANNEL_MIN_TIME)
    end_time = request.GET.get('end_time', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    data_grain = request.GET.get('data_grain', 'day')
    data_grain = data_grain if data_grain else 'day'
    
    if start_time == 'NaN-aN-aN aN:aN:aN': 
        start_time = c.SHARE_CHANNEL_MIN_TIME
    if end_time == 'NaN-aN-aN aN:aN:aN': 
        end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    data = get_share_channels(start_time, end_time, data_grain)
    response = HttpResponse(anyjson.dumps(data))
    
    # 缓存一天, 也只能缓存一天
    # 因为start_time和end_time可能是NA, 那么一天之后, 这个NA的数据实际上是会发生变化的.
    now = datetime.datetime.now()
    expire = now + datetime.timedelta(days=1)
    response['Expires'] = expire.strftime('%a, %d %b %Y 01:00:00 %Z')
    return response

# 综合 客户端分享统计
@login_required
def public_client(request):
    start_time = request.GET.get('start_time', c.SHARE_CHANNEL_MIN_TIME)
    end_time = request.GET.get('end_time', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    data_grain = request.GET.get('data_grain', 'day')
    data_grain = data_grain if data_grain else 'day'
    
    if start_time == 'NaN-aN-aN aN:aN:aN': 
        start_time = c.SHARE_CHANNEL_MIN_TIME
    if end_time == 'NaN-aN-aN aN:aN:aN': 
        end_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    data = get_public_client(start_time, end_time, data_grain)
    response = HttpResponse(anyjson.dumps(data))

    # 缓存一天, 也只能缓存一天
    # 因为start_time和end_time可能是NA, 那么一天之后, 这个NA的数据实际上是会发生变化的.
    now = datetime.datetime.now()
    expire = now + datetime.timedelta(days=1)
    response['Expires'] = expire.strftime('%a, %d %b %Y 01:00:00 %Z')
    return response

# 综合 收藏文章排行统计  
@login_required
def bookmark_per_user(request):
    start_time = request.GET.get('start_time', c.MIN_TIME)
    end_time = request.GET.get('end_time', c.MAX_TIME)
    limit = request.GET.get('data_size', '100')
    limit = int(limit if limit else 100)
    
    if start_time == 'NaN-aN-aN aN:aN:aN': 
        start_time = c.MIN_TIME
    if end_time == 'NaN-aN-aN aN:aN:aN': 
        end_time = c.MAX_TIME

    jsondata = get_bookmark_per_user(start_time, end_time, limit)
    
    response = HttpResponse(jsondata)
    # 缓存一天
    now = datetime.datetime.now()
    expire = now + datetime.timedelta(days=1)
    response['Expires'] = expire.strftime('%a, %d %b %Y 01:00:00 %Z')
    return response

# 综合 收藏文章时段统计
@login_required
def bookmark_time(request):
    start_time = request.GET.get('start_time', c.MIN_TIME)
    end_time = request.GET.get('end_time', c.MAX_TIME)
    
    if start_time == 'NaN-aN-aN aN:aN:aN': 
        start_time = c.MIN_TIME
    if end_time == 'NaN-aN-aN aN:aN:aN': 
        end_time = c.MAX_TIME
        
    jsondata = get_bookmark_time(start_time, end_time)
    
    response = HttpResponse(jsondata)
    # 缓存一天
    now = datetime.datetime.now()
    expire = now + datetime.timedelta(days=1)
    response['Expires'] = expire.strftime('%a, %d %b %Y 01:00:00 %Z')
    return response

# 综合 收藏文章百分比(pie)统计
@login_required
def user_bookmark_percent(request):
    start_time = request.GET.get('start_time', c.MIN_TIME)
    end_time = request.GET.get('end_time', c.MAX_TIME)
    
    if start_time == 'NaN-aN-aN aN:aN:aN': 
        start_time = c.MIN_TIME
    if end_time == 'NaN-aN-aN aN:aN:aN': 
        end_time = c.MAX_TIME
        
    jsondata = get_bookmark_percent(start_time, end_time, raw=False)

    response = HttpResponse(jsondata)
    # 缓存一天
    now = datetime.datetime.now()
    expire = now + datetime.timedelta(days=1)
    response['Expires'] = expire.strftime('%a, %d %b %Y 01:00:00 %Z')
    return response

'''深度统计'''

# 深度统计页面首页
@login_required
def depth(request):
    template = loader.get_template('statistics/depth.html')
    c = Context({
        'name': 'liubida'})
        
    return HttpResponse(template.render(c))

# 深度 活跃用户统计    
@login_required
def activate_user(request):
    start_time = request.GET.get('start_time', c.MIN_TIME)
    end_time = request.GET.get('end_time', c.MAX_TIME)
    data_grain = request.GET.get('data_grain', 'day')
    data_grain = data_grain if data_grain else 'day'
    
    if start_time == 'NaN-aN-aN aN:aN:aN': 
        start_time = c.MIN_TIME
    if end_time == 'NaN-aN-aN aN:aN:aN': 
        end_time = c.MAX_TIME

    jsondata = get_activate_user(start_time, end_time, data_grain=data_grain)

    response = HttpResponse(jsondata)
    # 缓存一天
    now = datetime.datetime.now()
    expire = now + datetime.timedelta(days=1)
    response['Expires'] = expire.strftime('%a, %d %b %Y 01:00:00 %Z')
    return response

# 深度 转化率统计    
@login_required
def conversion(request):
    start_time = request.GET.get('start_time', c.MIN_TIME)
    end_time = request.GET.get('end_time', c.MAX_TIME)
    data_grain = request.GET.get('data_grain', 'day')
    data_grain = data_grain if data_grain else 'day'
    
    if start_time == 'NaN-aN-aN aN:aN:aN': 
        start_time = c.MIN_TIME
    if end_time == 'NaN-aN-aN aN:aN:aN': 
        end_time = c.MAX_TIME

    jsondata = get_conversion(start_time, end_time, data_grain=data_grain)

    response = HttpResponse(jsondata)
    # 缓存一天
    now = datetime.datetime.now()
    expire = now + datetime.timedelta(days=1)
    response['Expires'] = expire.strftime('%a, %d %b %Y 01:00:00 %Z')
    return response

# 深度 收藏文章来源网站统计_PV
@login_required
def bookmark_website(request):
    start_time = request.GET.get('start_time', c.MIN_TIME)
    end_time = request.GET.get('end_time', c.MAX_TIME)
    limit = request.GET.get('size', '100')
    limit = int(limit if limit else 100)
    
    if start_time == 'NaN-aN-aN aN:aN:aN': 
        start_time = c.MIN_TIME
    if end_time == 'NaN-aN-aN aN:aN:aN': 
        end_time = c.MAX_TIME
    data = get_bookmark_website(start_time, end_time, limit=limit)
    jsondata = anyjson.dumps(data)
    
    response = HttpResponse(jsondata)
    # 缓存一天
    now = datetime.datetime.now()
    expire = now + datetime.timedelta(days=1)
    response['Expires'] = expire.strftime('%a, %d %b %Y 01:00:00 %Z')
    return response

def bookmark_website_detail(request):
    start_time = request.GET.get('start_time', c.MIN_TIME)
    end_time = request.GET.get('end_time', c.MAX_TIME)
    limit = request.GET.get('size', '100')
    limit = int(limit if limit else 100)
    
    if start_time == 'NaN-aN-aN aN:aN:aN': 
        start_time = c.MIN_TIME
    if end_time == 'NaN-aN-aN aN:aN:aN': 
        end_time = c.MAX_TIME
    
    data = get_bookmark_website_detail(start_time, end_time, limit=limit)
    s = { 'data': data }
                    
    t = loader.get_template('statistics/bookmark_website_detail_table.html')
    response = HttpResponse(t.render(Context({'s':s})))
    
    # 缓存一天
    now = datetime.datetime.now()
    expire = now + datetime.timedelta(days=1)
    response['Expires'] = expire.strftime('%a, %d %b %Y 01:00:00 %Z')
    return response

# 深度 收藏文章来源网站统计_UV
@login_required
def bookmark_website_for_user(request):
    start_time = request.GET.get('start_time', c.MIN_TIME)
    end_time = request.GET.get('end_time', c.MAX_TIME)
    limit = request.GET.get('size', '100')
    limit = int(limit if limit else 100)
    
    
    if start_time == 'NaN-aN-aN aN:aN:aN': 
        start_time = c.MIN_TIME
    if end_time == 'NaN-aN-aN aN:aN:aN': 
        end_time = c.MAX_TIME
    
    jsondata = get_bookmark_website_for_user(start_time, end_time, limit=limit)
        
    response = HttpResponse(jsondata)
    # 缓存一天
    now = datetime.datetime.now()
    expire = now + datetime.timedelta(days=1)
    response['Expires'] = expire.strftime('%a, %d %b %Y 01:00:00 %Z')
    return response

# 深度 用户使用平台统计
@login_required
def user_platform(request):
    start_time = request.GET.get('start_time', c.MIN_TIME)
    end_time = request.GET.get('end_time', c.MAX_TIME)
    
    if start_time == 'NaN-aN-aN aN:aN:aN': 
        start_time = c.MIN_TIME
    if end_time == 'NaN-aN-aN aN:aN:aN': 
        end_time = c.MAX_TIME
        
    jsondata = get_user_platform(start_time, end_time)
    
    response = HttpResponse(jsondata)
    # 缓存3小时
    now = datetime.datetime.now()
    expire = now + datetime.timedelta(hours=3)
    response['Expires'] = expire.strftime('%a, %d %b %Y %H:%M:%S %Z')
    return response

'''日报'''
# 日报首页页面
@login_required
def day_report(request):
    template = loader.get_template('statistics/day_report.html')
    c = Context({
        'name': 'liubida'})
        
    return HttpResponse(template.render(c))

# 日报日期
@login_required
def day_report_date(request):
    time_array = Report.objects.filter(type='day').values('time')
    
    day_array = []
    day_format = "%Y-%m-%d"
    for t in time_array:
        day_array.append(t['time'].strftime(day_format))

    s = {}
    s['success'] = True
    s['info'] = ''
    s['code'] = 0
    s['total'] = len(day_array)
    s['list'] = day_array
    
    response = HttpResponse(anyjson.dumps(s))
    # 缓存一天, url不会变, 但是数据是一天一变, 所以最多只能缓存一天
    # 新数据会在0点之后出来
    now = datetime.datetime.now()
    expire = now + datetime.timedelta(days=1)
    response['Expires'] = expire.strftime('%a, %d %b %Y 01:00:00 %Z')
    return response

# 日报概要信息    
@login_required
def day_report_abstract(request):
    start_time = request.GET.get('start_time', '')
    end_time = request.GET.get('end_time', '')
    
    if not start_time and not end_time: 
        end_time = datetime.datetime.today()
        start_time = end_time - datetime.timedelta(days=1)
    jsondata_array = Report.objects.filter(type='day', time__gte=start_time, time__lt=end_time).values('jsondata')
    if jsondata_array:
        jsondata = jsondata_array[0]['jsondata']
        data = anyjson.loads(jsondata)
        bookmark_new = data['bookmark']['total'] - data['bookmark']['total_yd']
        s = {
            'name': 'liubida',
            'user_total'    : data['user']['total'],
            'user_total_inc': data['user']['total_inc'],
            'user_new'      : data['user']['total'] - data['user']['total_yd'],
            'user_new_inc'  : data['user']['new_inc'],
            'user_new_inc_color': c.red if data['user']['new_inc'] > 0  else c.green,
            'bookmark_total'    : data['bookmark']['total'],
            'bookmark_total_inc': data['bookmark']['total_inc'],
            'bookmark_new'      : bookmark_new,
            'bookmark_new_inc'  : data['bookmark']['new_inc'],
            'bookmark_new_inc_color': c.red if data['bookmark']['new_inc'] > 0  else c.green,
            'email_total'        : '-' if not data.has_key('email') else data['email']['total'],
            'email_total_inc'    : '-' if not data.has_key('email') else data['email']['total_inc'],
            'email_new'          : '-' if not data.has_key('email') else data['email']['total'] - data['email']['total_yd'],
            'email_new_inc'      : '-' if not data.has_key('email') else data['email']['new_inc'],
            'email_new_inc_color': c.red if not data.has_key('emai') else (c.red if data['email']['new_inc'] > 0  else c.green),
            'fiction_total'      : '-' if not data.has_key('fiction') else data['fiction']['total'],
            'fiction_total_inc'  : '-' if not data.has_key('fiction') else data['fiction']['total_inc'],
            'fiction_new'        : '-' if not data.has_key('fiction') else data['fiction']['total'] - data['fiction']['total_yd'],
            'fiction_new_inc'    : '-' if not data.has_key('fiction') else data['fiction']['new_inc'],
            'fiction_new_inc_color': c.red if not data.has_key('fiction') else (c.red if data['fiction']['new_inc'] > 0  else c.green),
            'shorturl_total'      : '-' if not data.has_key('shorturl') else data['shorturl']['total'],
            'shorturl_total_inc'  : '-' if not data.has_key('shorturl') else data['shorturl']['total_inc'],
            'shorturl_new'        : '-' if not data.has_key('shorturl') else data['shorturl']['total'] - data['shorturl']['total_yd'],
            'shorturl_new_inc'    : '-' if not data.has_key('shorturl') else data['shorturl']['new_inc'],
            'shorturl_new_inc_color': c.red if not data.has_key('shorturl') else (c.red if data['shorturl']['new_inc'] > 0  else c.green),
            'set_public_total'      : '-' if not data.has_key('set_public') else data['set_public']['total'],
            'set_public_total_inc'  : '-' if not data.has_key('set_public') else data['set_public']['total_inc'],
            'set_public_new'        : '-' if not data.has_key('set_public') else data['set_public']['total'] - data['set_public']['total_yd'],
            'set_public_new_inc'    : '-' if not data.has_key('set_public') else data['set_public']['new_inc'],
            'set_public_new_inc_color': c.red if not data.has_key('set_public') else (c.red if data['set_public']['new_inc'] > 0  else c.green),
        }
        
        try:
            bookmark_failed_count = len(data['bookmark']['failed'])
            s['bookmark_failed_count'] = bookmark_failed_count
            
            bookmark_failed_percent = (bookmark_failed_count + 0.00000001) / bookmark_new
            bookmark_failed_percent = round(bookmark_failed_percent, 4)
            s['bookmark_failed_percent'] = bookmark_failed_percent

            s['bookmark_failed'] = data['bookmark']['failed']
        except Exception:
            s['bookmark_failed_count'] = 0
            s['bookmark_failed_percent'] = 0
            s['bookmark_failed'] = None            
        
        response = HttpResponse(anyjson.dumps(s))
        # 这是旧时的数据, 可以永久缓存
        now = datetime.datetime.now()
        expire = now + datetime.timedelta(days=7)
        response['Expires'] = expire.strftime('%a, %d %b %Y %H:%M:%S %Z')
        return response
    
# 日报收藏文章比例        
@login_required
def day_report_bookmark_percent(request):
    start_time = request.GET.get('start_time', '')
    end_time = request.GET.get('end_time', '')
    
    jsondata_array = Report.objects.filter(type='day', time__gte=start_time, time__lt=end_time).values('jsondata')
    if jsondata_array:
        jsondata = jsondata_array[0]['jsondata']
        data = anyjson.loads(jsondata)
        response = HttpResponse(anyjson.dumps(data['bookmark_count']))
        
        # 这是旧时的数据, 可以永久缓存
        now = datetime.datetime.now()
        expire = now + datetime.timedelta(days=7)
        response['Expires'] = expire.strftime('%a, %d %b %Y %H:%M:%S %Z')
        return response        

# 日报收藏文章来源网站    
@login_required
def day_report_bookmark_website(request):
    start_time = request.GET.get('start_time', '')
    end_time = request.GET.get('end_time', '')
    
    jsondata_array = Report.objects.filter(type='day', time__gte=start_time, time__lt=end_time).values('jsondata')
    if jsondata_array:
        jsondata = jsondata_array[0]['jsondata']
        data = anyjson.loads(jsondata)
        response = HttpResponse(anyjson.dumps(data['bookmark_website']))
        
        # 这是旧时的数据, 可以永久缓存
        now = datetime.datetime.now()
        expire = now + datetime.timedelta(days=7)
        response['Expires'] = expire.strftime('%a, %d %b %Y %H:%M:%S %Z')
        return response        
        

'''周报'''
  
# 周报首页
@login_required
def week_report(request):
    template = loader.get_template('statistics/week_report.html')
    c = Context({
        'name': 'liubida'})
        
    return HttpResponse(template.render(c))

# 周报日期
@login_required
def week_report_date(request):
    t = loader.get_template('statistics/week_report_date.html')

    week_list = _get_week_list(end=datetime.datetime.now()) 
    
    response = HttpResponse(t.render(Context({'week_list':week_list})))
    return response

# 周报综合
@login_required
def week_report_abstract(request):
    start_time = request.GET.get('start_time', '2012-07-16')
    # 注意, 周报表里面的time是当时统计周报数据的时间, 所以记录的数据实际是相对time上一周的数据
    # request里请求的时间是7-16, 则实际存储的周报时间是7-23
    start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d')
    start_time = start_time + datetime.timedelta(days=7)
    end_time = start_time + datetime.timedelta(days=2)

    jsondata_array = Report.objects.filter(type='week', time__gte=start_time, time__lt=end_time).values('jsondata')
    if jsondata_array:
        jsondata = jsondata_array[0]['jsondata']
        data = anyjson.loads(jsondata)
        
        purify_timeout_bookmarks = [];
        purify_error_bookmarks = [];
        
        for b in data['failed_bookmark']:
            
            pass
                    
        s = {
            'name': 'liubida',
            'new_user'    : data['new_user'],
            'new_bookmark'    : data['new_bookmark'],
            'add_way_and_platform' : data['add_way_and_platform']['data']
        }
        try:
            s['failed_bookmark'] = data['failed_bookmark']
        except Exception, e:
            s['failed_bookmark'] = None
                        
        t = loader.get_template('statistics/week_report_abstract.html')
        response = HttpResponse(t.render(Context({'s':s})))
        return response
        
#        # 这是旧时的数据, 可以永久缓存
#        now = datetime.datetime.now()
#        expire = now + datetime.timedelta(days=7)
#        response['Expires'] = expire.strftime('%a, %d %b %Y %H:%M:%S %Z')
#        return response

# 周报收藏文章来源网站    
@login_required
def week_report_bookmark_website(request):
    start_time = request.GET.get('start_time', '2012-07-16 00:00:00')
    # 注意, 周报表里面的time是当时统计周报数据的时间, 所以记录的数据实际是相对time上一周的数据
    # 那么我要查7-16这一周的数据, time就应该为7-23
    start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    start_time = start_time + datetime.timedelta(days=7)
    end_time = start_time + datetime.timedelta(days=2)
    
    jsondata_array = Report.objects.filter(type='week', time__gte=start_time, time__lt=end_time).values('jsondata')
    if jsondata_array:
        jsondata = jsondata_array[0]['jsondata']
        data = anyjson.loads(jsondata)
        response = HttpResponse(anyjson.dumps(data['bookmark_website']))
        return response
#        # 这是旧时的数据, 可以永久缓存
#        now = datetime.datetime.now()
#        expire = now + datetime.timedelta(days=7)
#        response['Expires'] = expire.strftime('%a, %d %b %Y %H:%M:%S %Z')
#        return response        

@login_required
def week_report_bookmark_failed(request):
    start_time = request.GET.get('start_time', '2012-07-16 00:00:00')
    # 注意, 周报表里面的time是当时统计周报数据的时间, 所以记录的数据实际是相对time上一周的数据
    # 那么我要查7-16这一周的数据, time就应该为7-23
    start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    start_time = start_time + datetime.timedelta(days=7)
    end_time = start_time + datetime.timedelta(days=2)
    
    jsondata_array = Report.objects.filter(type='week', time__gte=start_time, time__lt=end_time).values('jsondata')
    if jsondata_array:
        jsondata = jsondata_array[0]['jsondata']
        data = anyjson.loads(jsondata)
        response = HttpResponse(anyjson.dumps(data['']))
        return response
#        # 这是旧时的数据, 可以永久缓存
#        now = datetime.datetime.now()
#        expire = now + datetime.timedelta(days=7)
#        response['Expires'] = expire.strftime('%a, %d %b %Y %H:%M:%S %Z')
#        return response
        
        
        
        
        
# 编码时测试用
@login_required
def test(start_time, end_time, data_grain='day'):
    if start_time == 'NaN-aN-aN aN:aN:aN': 
        start_time = c.MIN_TIME
    if end_time == 'NaN-aN-aN aN:aN:aN': 
        end_time = c.MAX_TIME
    data = {'list':[]}
    raw_data = SomeTotal.objects.filter(name='user', time__gte=start_time, time__lte=end_time).values('time', 'count')
    
    if data_grain == 'hour':
        for d in raw_data:
            data['list'].append({'time':d['time'].strftime('%m-%d %H:%M:%S'), 'count':d['count']})
    elif data_grain == 'day':
        delta = datetime.timedelta(days=1)
        # 每天取一个23点的数据
        data['list'] = get_data_interval(raw_data, delta)
    elif data_grain == 'week':
        week_start = get_week_num(raw_data[0]['time'])
        
        first_day = datetime.date.today().replace(month=1, day=1)
        day = first_day + datetime.timedelta(weeks=week_start)
        
        for d in raw_data:
            if d['time'].hour == 23 and \
               d['time'].year == day['time'].year and \
               d['time'].month == day['time'].month and \
               d['time'].day == day['time'].day:
                data['list'].append({'time':d['time'].strftime('%Y-%m-%d'), 'count':d['count']})
                day += delta
        
#        # 每隔7天取一个23点的数据
#        delta = datetime.timedelta(days=7)
#        data['list'] = get_data_interval(raw_data, delta)
    elif data_grain == 'month':
        # 每隔4周天取一个23点的数据
        delta = datetime.timedelta(weeks=4)
        data['list'] = get_data_interval(raw_data, delta)
    
@login_required
def bookmark_shorturl(request):
    start_time = request.GET.get('start_time', c.MIN_TIME)
    end_time = request.GET.get('end_time', c.MAX_TIME)
    data_grain = request.GET.get('data_grain', 'day')
    data_grain = data_grain if data_grain else 'day'
    
    if start_time == 'NaN-aN-aN aN:aN:aN': 
        start_time = c.MIN_TIME
    if end_time == 'NaN-aN-aN aN:aN:aN': 
        end_time = c.MAX_TIME

    data = {'list':[]}
    raw_data = SomeTotal.objects.filter(name='shorturl', time__gte=start_time, time__lte=end_time).values('time', 'count')
    
    if data_grain == 'hour':
        for d in raw_data:
            data['list'].append({'time':d['time'].strftime('%m-%d %H:%M:%S'), 'count':d['count']})
    elif data_grain == 'day':
        delta = datetime.timedelta(days=1)
        # 每天取一个23点的数据
        data['list'] = get_data_interval(raw_data, delta)
    elif data_grain == 'week':
        # 每隔7天取一个23点的数据
        delta = datetime.timedelta(days=7)
        data['list'] = get_data_interval(raw_data, delta)
    elif data_grain == 'month':
        # 每隔4周天取一个23点的数据
        delta = datetime.timedelta(weeks=4)
        data['list'] = get_data_interval(raw_data, delta)

    # 计算data的增长率
    add_inc_for_data(data)
    
    response = HttpResponse(anyjson.dumps(data))
    # 缓存一天, 也只能缓存一天
    # 因为start_time和end_time可能是NA, 那么一天之后, 这个NA的数据实际上是会发生变化的.
    now = datetime.datetime.now()
    expire = now + datetime.timedelta(days=1)
    response['Expires'] = expire.strftime('%a, %d %b %Y 01:00:00 %Z')
    return response

@login_required
def bookmark_set_public(request):
    start_time = request.GET.get('start_time', c.MIN_TIME)
    end_time = request.GET.get('end_time', c.MAX_TIME)
    data_grain = request.GET.get('data_grain', 'day')
    data_grain = data_grain if data_grain else 'day'
    
    if start_time == 'NaN-aN-aN aN:aN:aN': 
        start_time = c.MIN_TIME
    if end_time == 'NaN-aN-aN aN:aN:aN': 
        end_time = c.MAX_TIME

    data = {'list':[]}
    raw_data = SomeTotal.objects.filter(name='set-public', time__gte=start_time, time__lte=end_time).values('time', 'count')
    
    if data_grain == 'hour':
        for d in raw_data:
            data['list'].append({'time':d['time'].strftime('%m-%d %H:%M:%S'), 'count':d['count']})
    elif data_grain == 'day':
        delta = datetime.timedelta(days=1)
        # 每天取一个23点的数据
        data['list'] = get_data_interval(raw_data, delta)
    elif data_grain == 'week':
        # 每隔7天取一个23点的数据
        delta = datetime.timedelta(days=7)
        data['list'] = get_data_interval(raw_data, delta)
    elif data_grain == 'month':
        # 每隔4周天取一个23点的数据
        delta = datetime.timedelta(weeks=4)
        data['list'] = get_data_interval(raw_data, delta)

    # 计算data的增长率
    add_inc_for_data(data)
    
    response = HttpResponse(anyjson.dumps(data))
    # 缓存一天, 也只能缓存一天
    # 因为start_time和end_time可能是NA, 那么一天之后, 这个NA的数据实际上是会发生变化的.
    now = datetime.datetime.now()
    expire = now + datetime.timedelta(days=1)
    response['Expires'] = expire.strftime('%a, %d %b %Y 01:00:00 %Z')
    return response

if __name__ == '__main__':
    test('NaN-aN-aN aN:aN:aN', 'NaN-aN-aN aN:aN:aN', 'week')
#    test('2012-07-12', '2012-07-17')
#    day_report_job()
#    mysql_ping_job();
#    user_total_job()
#    bookmark_total_job()
#    add_and_read_alarm_job()
#    url = RandomSpider().get_valid_url()
