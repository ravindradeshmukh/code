from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
	context=RequestContext(request)
	context_dict={'boldmessage': "I am bold font from the context"}
	return render_to_response('rango/index.html', context_dict, context)
	#response="Rango says Hello <a href='/rango/about/'>About</a>"
	#return HttpResponse(response)

def about(request):
	context=RequestContext(request)	
	#response="Rango says: Here is the about page <a href='/rango/'>Home</a>"
	return render_to_response('rango/about.html', context)
	#return HttpResponse(response)

