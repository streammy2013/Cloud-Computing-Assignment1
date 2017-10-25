from django.shortcuts import render
from django.http import HttpResponse

import simplejson as json
from twitteres.twitter_streaming import TweetStream, MyTwitterHandler
from twitteres.ElasticSearchWrapper import ElasticSearchWrapper
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import types

import threading

def index(request):
	return render(request,"myTwittMap/index.html")

es = ElasticSearchWrapper()

def start_streaming():
    es = ElasticSearchWrapper()   
    h = MyTwitterHandler(es)
    #h.get_count()
    s = TweetStream()
    s.set_handle(h)
    s.start_stream()

t = threading.Thread(target = start_streaming)
t.setDaemon(True)
t.start()

def show_stored(request):
	
	response = es.fetch_stored(1000)
	response = response['hits']['hits']
	response = json.dumps(response)
	return HttpResponse(response, content_type='json')

def search(request):
	
	keyword = request.POST['keyword']
	response = es.search(keyword)
	response = response['hits']['hits']
	response = json.dumps(response)
	return HttpResponse(response, content_type='json')

def geosearch(request):
	distance = request.POST.get('distance')
	location = request.POST.get('location')
	response = es.geosearch(distance, location)
	result = response['hits']['hits']
	return HttpResponse(json.dumps(result), content_type='json')
# Create your views here.
