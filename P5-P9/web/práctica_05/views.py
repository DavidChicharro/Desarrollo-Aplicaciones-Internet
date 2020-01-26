from django.shortcuts import render, redirect, HttpResponse
from django.core.paginator import Paginator

from .models import Grupo,Musico,Album
from .forms import GrupoForm,MusicoForm,AlbumForm
from django.http import JsonResponse
import json

import logging
logger = logging.getLogger(__name__)

# Create your views here.
def get_username(request):
	username=''
	if request.user.is_authenticated:
		username = request.user.username

	return username

def index(request):
	return HttpResponse('Hello World!')

def test_template(request):
	username = get_username(request)

	grupos = Grupo.objects.all()
	context = {'grupos':grupos, 'username':username}   # Aquí van la las variables para la plantilla
	return render(request,'test.html', context)

def aniadir_grupo(request):
	username = get_username(request)
	if request.method == "POST":
		form = GrupoForm(request.POST)
		if form.is_valid():
			post = form.save(commit=True)
			post.save()
			context = {'pk':post.pk, 'username':username}
			return redirect('/miaplicacion', context)
	else:
		form = GrupoForm()

	context = {'form': form, 'username':username}
	return render(request,'add_grupo.html',context)

def aniadir_musico(request):
	username = get_username(request)
	if request.method == "POST":
		form = MusicoForm(request.POST)
		if form.is_valid():
			post = form.save(commit=True)
			post.save()
			context = {'pk':post.pk, 'username':username}
			return redirect('/miaplicacion', context)
	else:
		form = MusicoForm()

	context = {'form': form, 'username':username}
	return render(request,'add_grupo.html',context)


def aniadir_album(request):
	username = get_username(request)
	if request.method == "POST":
		form = AlbumForm(request.POST)
		if form.is_valid():
			post = form.save(commit=True)
			post.save()
			return redirect('/miaplicacion/grupos', pk=post.pk)
	else:
		form = AlbumForm()

	context = {'form': form, 'username':username}
	return render(request,'add_grupo.html',context)

def grupos_ajax(request):
	page = request.GET.get('page')
	if page == None:
		page=1
	else:
		page = int(page)

	lista_grupos = Grupo.objects.all()
	num_grupos = lista_grupos.count()
	grupos_x_pag = 2

	if (num_grupos%grupos_x_pag == 0):
		total_pags = int(num_grupos/grupos_x_pag)
	else:
		total_pags = int((num_grupos/grupos_x_pag)+1)

	list_pags = list(range(1,total_pags+1))

	g_desde = (page-1)*grupos_x_pag
	g_hasta = (page*grupos_x_pag)-1

	grupos = []
	for i in range (g_desde,g_hasta+1):
		grupo_actual = list([lista_grupos[i].nombre_grupo,
							lista_grupos[i].fecha_fundacion.strftime("%-d de %B de %Y"),
							lista_grupos[i].estilo_musical,
							lista_grupos[i].sitio_web])
		grupos.append(grupo_actual)
		if num_grupos == g_hasta:
			break

	datos = {'grupos':grupos, 'paginas':list_pags, 'current':page}
	datos_json = json.dumps(datos)

	return JsonResponse(datos_json, safe=False)

def mapas(request):
	username = get_username(request)
	context = {'username':username}
	return render(request,'mapas.html', context)

def graficas(request):
	username = get_username(request)

	'''
	Número de álbumes por grupo
	'''
	lista_grupos = Grupo.objects.all()
	albums_por_grupo = []

	for grupo in lista_grupos:
		num_albums = Album.objects.filter(grupo__nombre_grupo=grupo.nombre_grupo).count()
		albums_por_grupo.append([grupo.nombre_grupo,num_albums])


	'''
	Número de álbumes lanzados cada año
	'''
	lista_albumes = Album.objects.all()
	list_years = []
	for album in lista_albumes:
		list_years.append(int(album.fecha_lanzamiento.strftime('%Y')))

	min_year = min(list_years)
	max_year = max(list_years)
	dict_all = {i:0 for i in range (min_year,max_year+1)}

	years_with_albums = {i:list_years.count(i) for i in list_years}
	for key in years_with_albums:
		dict_all[key] = years_with_albums[key]

	all_years = list(dict_all.keys())
	list_count_albums = list(dict_all.values())


	context = {'username':username, 'albums_por_grupo':albums_por_grupo, 'alb_years':all_years, 'alb_cnt':list_count_albums}
	return render(request,'graficas.html', context)

def grupos(request):
	username = get_username(request)

	page = request.GET.get('page')
	if page == None:
		page=1
	else:
		page = int(page)

	lista_grupos = Grupo.objects.all()
	num_grupos = lista_grupos.count()
	grupos_x_pag = 2

	if (num_grupos%grupos_x_pag == 0):
		total_pags = int(num_grupos/grupos_x_pag)
	else:
		total_pags = int((num_grupos/grupos_x_pag)+1)

	list_pags = list(range(1,total_pags+1))

	g_desde = (page-1)*grupos_x_pag
	g_hasta = (page*grupos_x_pag)-1

	grupos = []
	for i in range (g_desde,g_hasta+1):
		grupos.append(lista_grupos[i])
		if num_grupos == g_hasta:
			break

	context = {'grupos':grupos, 'username':username, 'paginas':list_pags, 'current':page}
	return render(request,'grupos.html', context)

def login(request):
	return redirect('/accounts/login')

def registro(request):
	return redirect('/accounts/signup')

def logout(request):
	return redirect('/accounts/logout')
