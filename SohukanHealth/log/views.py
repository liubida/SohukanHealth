# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render_to_response

collection = dict()

def collector(request):
    print request
    global collection
    url = request.GET.get('url', None)
    data = request.GET.get('log', None)
    if collection.has_key(url):
        collection[url].append(data)
    else:
        collection[url] = [data]
    return HttpResponse()

def logger(request):
    return render_to_response('collector.html', globals())