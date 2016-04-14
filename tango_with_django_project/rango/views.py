from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from rango.models import Category

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    context_dict = {'categories': category_list}

    return render(request, 'rango/index.html', context_dict)

def about(request):
	context=RequestContext(request)	
	#response="Rango says: Here is the about page <a href='/rango/'>Home</a>"
	return render_to_response('rango/about.html', context)
	#return HttpResponse(response)

