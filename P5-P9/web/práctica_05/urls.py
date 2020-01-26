# miaplicacion/urls.py

from django.conf.urls import url, include

from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^test_template/$', views.test_template, name='test_template'),
	url(r'^add_grupo/$',views.aniadir_grupo,name='add_grupo'),
	url(r'^add_musico/$',views.aniadir_musico,name='add_musico'),
	url(r'^add_album/$',views.aniadir_album,name='add_album'),
	url(r'^grupos/$',views.grupos,name='grupos'),
	url(r'^grupos_ajax/',views.grupos_ajax,name='grupos_ajax'),
	url(r'^mapas/',views.mapas,name='mapas'),
	url(r'^graficas/',views.graficas,name='graficas'),
	url(r'^login$',views.login,name='login'),
	url(r'^registro$',views.registro,name='registro'),
	url(r'^logout$',views.logout,name='logout'),
]
