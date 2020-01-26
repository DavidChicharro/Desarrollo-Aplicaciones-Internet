from django import forms

from .models import Grupo,Musico,Album

YEARS = [x for x in range(1900,2020)]

class GrupoForm(forms.ModelForm):
	fecha_fundacion = forms.DateField(label='Fecha de fundación', widget=forms.SelectDateWidget(years=YEARS))
	#origen_grupo_lat = forms.FloatField(label='Origen (lat)')
	#origen_grupo_long = forms.FloatField(label='Origen (long)')
	class Meta:
		model = Grupo
		#fields = ('nombre_grupo', 'fecha_fundacion','estilo_musical','origen_grupo_lat','origen_grupo_long','sitio_web')
		fields = ('nombre_grupo', 'fecha_fundacion','estilo_musical','sitio_web')


class MusicoForm(forms.ModelForm):
	nombre_musico = forms.CharField(label='Nombre del músico')
	fecha_nacimiento = forms.DateField(label='Fecha de nacimiento', widget=forms.SelectDateWidget(years=YEARS))
	instrumento_ppal = forms.CharField(label='Instrumento principal')
	class Meta:
		model = Musico
		fields = ('nombre_musico', 'grupo','fecha_nacimiento','instrumento_ppal')


class AlbumForm(forms.ModelForm):
	titulo_album = forms.CharField(label='Título del álbum')
	fecha_lanzamiento = forms.DateField(label='Fecha de lanzamiento', widget=forms.SelectDateWidget(years=YEARS))
	class Meta:
		model = Album
		fields = ('titulo_album', 'grupo','distribuidora','fecha_lanzamiento')