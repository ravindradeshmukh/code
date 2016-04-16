from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from rango.models import Category, Page, UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rango.forms import CategoryForm, PageForm, UserProfileForm,UserForm


def index(request):
    	context_dict={}
	try:
		category_list = Category.objects.order_by('-likes')[:5]
    		page_list = Page.objects.order_by('-views')[:5]
    		context_dict['categories']=category_list
    		context_dict['pages']=page_list
	except Category.DoesNotExists:
		pass
    	return render(request, 'rango/index.html', context_dict)

def about(request):
	context=RequestContext(request)	
	#response="Rango says: Here is the about page <a href='/rango/'>Home</a>"
	return render_to_response('rango/about.html', context)
	#return HttpResponse(response)

def category(request,category_name_slug):
	context_dict={}
	try:
		category=Category.objects.get(slug=category_name_slug)
		context_dict['category_name']=category.name
		pages=Page.objects.filter(category=category)
		context_dict['pages']=pages
		context_dict['category']=category
	except Category.DoesNotExists:
		pass
	return render(request, 'rango/category.html', context_dict)

def add_category(request):
	
	if request.method == "POST":
		form=CategoryForm(request.POST)
	
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/rango/')
		else:
			print form.errors
	else:
		form=CategoryForm()
	return render(request, 'rango/add_category.html', {'form': form})

def add_page(request,category_name_slug):

	try:
		cat=Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExists:
		cat=None
	
	if request.method=='POST':
		form=PageForm(request.POST)
		if form.is_valid():
			if cat:
				page=form.save(commit=False)
				page.category=cat
				page.save()
				return category(request, category_name_slug)
		else:
			print form.errors
	else:
		form=PageForm()
	context_dict={'form':form, 'category': cat}
	return render(request, 'rango/add_page.html', context_dict)

def register(request):
	registered=False
	if request.method=='POST':
		user_form=UserForm(data=request.POST)
		profile_form=UserProfileForm(data=request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			user=user_form.save()
			user.set_password(user.password)
			user.save()
			profile=profile_form.save(commit=False)
			profile.user=user
			if 'picture' in request.FILES:
				profile.picture=request.FILES['picture']
			profile.save()
			registered=True
		else:
			print user_form.errors, profile_form.errors
	else:
		user_form=UserForm()
		profile_form=UserProfileForm()
	return render(request,'rango/register.html',{'user_form':user_form,'profile_form':profile_form,  'registered':registered})

def user_login(request):
	if request.method=='POST':
		username=request.POST.get('username')
		password=request.POST.get('password')
		user=authenticate(username=username,password=password)
		if user:
			if user.is_active:
				login(request,user)
				return HttpResponseRedirect('/rango/?login_successful')
			else:
				error_msg="Your Rango account is disabled."
				return render(request,'rango/login.html',{'error_msg':error_msg})
				
		else:
			error_msg="Invalid login details supplied."
			return render(request,'rango/login.html',{'error_msg':error_msg})	
	else:
		return render(request,'rango/login.html',{})

def some_view(request):
	if not request.user.is_authenticated():
		return HttpResponse("You are not logged in.")
	else:
		return HttpResponse("You are not logged in.")
@login_required
def restricted(request):
	return HttpResponseRedirect("Since you're logged in, you can see this text")


def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/rango/?logout_successful')
		



