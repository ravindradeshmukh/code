from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from rango.models import Category, Page, UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from rango.forms import CategoryForm, PageForm, UserProfileForm,UserForm
from rango.bing_search import run_query

def index(request):

	category_list=Category.objects.order_by('-likes')[:5]
	page_list=Page.objects.order_by('-views')[:5]
	context_dict={'categories':category_list, 'pages':page_list}
	visits=request.session.get('visits')

	if not visits:
		visits=1

	reset_last_visit_time=False
	last_visit=request.session.get('last_visit')
	
	if last_visit:
		last_visit_time=datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

		if(datetime.now() - last_visit_time).seconds > 0:
			visits +=1
			reset_last_visit_time=True

	else:
		reset_last_visit_time=True

	if reset_last_visit_time:
		request.session['last_visit']=str(datetime.now())
		request.session['visits']=visits

	context_dict['visits']=visits
	response=render(request,'rango/index.html',context_dict)
	return response

def about(request):
	context=RequestContext(request)	
	#response="Rango says: Here is the about page <a href='/rango/'>Home</a>"
	return render_to_response('rango/about.html', context)
	#return HttpResponse(response)

def category(request,category_name_slug):
	result_list=[]
	if request.method=='POST' :
		try:
			category=request.POST['category'].strip()
			if category:
				category=Category.objects.get(slug=category_name_slug)
				context_dict['category_name']=category.name
				pages=Page.objects.filter(category=category).order_by('views')
				context_dict['pages']=pages
				context_dict['category']=category
		except Category.DoesNotExists:
				pass
		return render(request,'rango/search.html',{'result_list': result_list})
	else:
		context_dict={}
		try:
			category=Category.objects.get(slug=category_name_slug)
			context_dict['category_name']=category.name
			pages=Page.objects.filter(category=category)
			category.views+=1
			category.save()
			context_dict['pages']=pages
			context_dict['category']=category
		except Category.DoesNotExists:
			pass
		return render(request, 'rango/category.html', context_dict)

def category_list(request):
	context_dict={}
	categories=Category.objects.all()
	context_dict['categories']=categories
	return render(request, 'rango/category_list.html', context_dict)
	
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
			# if 'picture' not in request.FILES:
				# profile.picture=request.FILES[picture]
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
	
	
def search(request):
	result_list=[]
	if request.method=='POST' :
		query=request.POST['query'].strip()
		if query:
			result_list=run_query(query)
	return render(request,'rango/search.html',{'result_list': result_list})

def track(request, page_id):
	pages=Page.objects.get(id=page_id)
	pages.views+=1
	pages.save()
	return HttpResponseRedirect(pages.url)
	
def category_search(request):
	context_dict={}
	categories=Category.objects.all()
	if request.method=='POST':
		cat=request.POST['cat']
		context_dict['cat']=cat
	context_dict['category_list']=categories
	return render(request, 'rango/category_search.html', context_dict)	

# @login_required
# def like_category(request):

#     cat_id = None
#     if request.method == 'GET':
#         cat_id = request.GET['category_id']

#     likes = 0
#     if cat_id:
#         cat = Category.objects.get(id=int(cat_id))
#         if cat:
#             likes = cat.likes + 1
#             cat.likes =  likes
#             cat.save()

#     return HttpResponse(likes)

# def get_category_list(max_results=0, starts_with=''):
#         cat_list = []
#         if starts_with:
#                 cat_list = Category.objects.filter(name__istartswith=starts_with)

#         if max_results > 0:
#                 if cat_list.count() > max_results:
#                         cat_list = cat_list[:max_results]

#         return cat_list

# def suggest_category(request):

#         cat_list = []
#         starts_with = ''
#         if request.method == 'GET':
#                 starts_with = request.GET['suggestion']

#         cat_list = get_category_list(8, starts_with)

#         return render(request, 'rango/cats.html', {'cat_list': cat_list })

def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/rango/?logout_successful')
		



