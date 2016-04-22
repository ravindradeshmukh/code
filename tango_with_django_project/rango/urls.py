from django.conf.urls import patterns,url,include
from rango import views

urlpatterns=[ 
	url(r'^$', views.index, name='index'),
	url(r'^about/', views.about, name='about'),
	url(r'^category_list/$', views.category_list, name='category_list'),
	url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
	url(r'^add_category/$', views.add_category, name='add_category'), 
	url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
	url(r'^restricted/',views.restricted,name='restricted'),
	url(r'^register/',views.register, name='register'),
	url(r'^login/', views.user_login, name='login'),
	url(r'^search/', views.search, name='search'),
	url(r'^goto/(?P<page_id>[\w\-]+)/$',views.track, name='goto'),
	url(r'^category_search/',views.category_search, name='category_search'),
	# url(r'^like_category/$', views.like_category, name='like_category'),

	
]

