'''
Created on Jun 14, 2012

@author: liubida
'''
from django.http import HttpResponse, Http404
from django.template import loader
from django.template.context import Context
import datetime

def home_page(request):
    return HttpResponse("hi, i'm at home!")

def hello(request):
    return HttpResponse("hello liubida")

def now(request):
    now = datetime.datetime.now()
    return HttpResponse("now is : %s " % now)

def now_plus(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    assert True
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    return HttpResponse("now + %s is : %s " % (offset, dt))

def demo(request):
#    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    
    t = loader.get_template('JSCharts3_demo/examples/line-charts/example-1/index.html')
    c = Context({
        'name': 'liubida&&zww',
    })
    return HttpResponse(t.render(c))

def index(request):
    t = loader.get_template('index.html')
    c = Context()
    return HttpResponse(t.render(c))

def about(request):
    t = loader.get_template('about.html')
    c = Context()
    return HttpResponse(t.render(c))
    
#    
#class JSONResponseMixin(object):
#    """
#    A mixin that can be used to render a JSON response.
#    """
#    reponse_class = HTTPResponse
#
#    def render_to_response(self, context, **response_kwargs):
#        """
#        Returns a JSON response, transforming 'context' to make the payload.
#        """
#        response_kwargs['content_type'] = 'application/json'
#        return self.response_class(
#            self.convert_context_to_json(context),
#            **response_kwargs
#        )
#
#    def convert_context_to_json(self, context):
#        "Convert the context dictionary into a JSON object"
#        # Note: This is *EXTREMELY* naive; in reality, you'll need
#        # to do much more complex handling to ensure that arbitrary
#        # objects -- such as Django model instances or querysets
#        # -- can be serialized as JSON.
#        return json.dumps(context)
#    
#class JSONView(JSONResponseMixin, View):
#    
#    pass