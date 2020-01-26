from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from django.utils import timezone

class Grupo(models.Model):
	nombre_grupo = models.CharField(
		max_length=60, primary_key=True)
	fecha_fundacion = models.DateField(
		blank=True, null=True) 
	estilo_musical = models.CharField(max_length=30)
	#origen_grupo_lat = models.FloatField(validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)],blank=True, null=True)
	#origen_grupo_long = models.FloatField(validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)],blank=True, null=True)
	sitio_web = models.CharField(max_length=80)

	def xxx(self):
		self.save()

	def __str__(self):
		return self.nombre_grupo

class Musico(models.Model):
	nombre_musico = models.CharField(
		max_length=200, primary_key=True)
	grupo = models.ForeignKey('Grupo', on_delete=models.CASCADE)
	fecha_nacimiento = models.DateField(
		blank=True, null=True)
	instrumento_ppal = models.CharField(max_length=30)

	def yyy(self):
		self.save()

	def __str__(self):
		return self.nombre_musico

class Album(models.Model):
	titulo_album = models.CharField(
		max_length=150, primary_key=True)
	grupo = models.ForeignKey('Grupo', on_delete=models.CASCADE)
	distribuidora = models.CharField(max_length=100)
	fecha_lanzamiento = models.DateField(
		blank=True, null=True)

	def get_year_album(self):
		return self.fecha_lanzamiento.year

	def zzz(self):
		self.save()

	def __str__(self):
		return self.titulo_album