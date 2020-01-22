from django.conf.urls import url
from . import views
from django.views.generic import CreateView
from django.contrib.auth import views as auth_views
from .models import MyModel


urlpatterns=[url(r'^$',views.index,name='index'),
	 url(r'^home/$', views.homepage.as_view(model=MyModel,success_url='/display/'), name='homepage'),
	 url(r'^login/$', auth_views.login, name='login'),
     url(r'^logout/$', auth_views.logout,{'next_page': 'index'}, name='logout'),
     url(r'^signup/$', views.Signup.as_view(), name='signup'),
	 url(r'^dashboard/$', views.dashboard, name='dashboard'),
	 url(r'^hotels/$', views.hotels, name='hotels'),
	 url(r'^restaurants/$', views.restaurants, name='restaurants'),
	 url(r'^display/$', views.display, name='display'),
	 url(r'^recommendation_r/$', views.recommendation_r, name='recommendation_r'),
url(r'^recommendation_h/$', views.recommendation_h, name='recommendation_h'),
	 url(r'^mapdisplay/$',views.mapdisplay, name='mapdisplay'),
	 url(r'^distancecalc/$',views.distancecalc, name='distancecalc'),
     url(r'^dirdisplay/$',views.dirdisplay, name='dirdisplay'),
	 url(r'^placedisplay/$',views.placedisplay, name='placedisplay'),
url(r'^hoteldisplay/$',views.hoteldisplay, name='hoteldisplay'),
url(r'^restdisplay/$',views.restdisplay, name='restdisplay'),
url(r'^ratingsubmit/$',views.ratingsubmit, name='ratingsubmit'),
url(r'^filter/$',views.filter, name='filter'),
url(r'^nearbyrec/$',views.nearbyrec, name='nearbyrec')
			 ]
