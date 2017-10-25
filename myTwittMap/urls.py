from django.conf.urls import url
from . import views
from django.views.decorators.csrf import csrf_exempt 
urlpatterns = [
	url(r'^$',views.index, name = 'index'),
	url(r'^ajax/show_stored', views.show_stored, name='show_stored'),
	url(r'^ajax/search', views.search, name='search'),
	url(r'^ajax/geosearch',views.geosearch, name='geosearch'),
]