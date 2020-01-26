#!/usr/bin/python
# -*- coding: utf-8 -*-

# Practicas de Desarrollo de Aplicaciones para Internet (DAI)
# Copyright (C) 2013 - 2018 - Zerjillo (zerjioi@ugr.es)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#import time
from PIL import Image

# Función que pinta en una ventana y salva en formato PPM el fractal de Mandelbrot. Nota: iteraciones tiene que ser menor que 1000
def pintaMandelbrot(x1, y1, x2, y2, ancho, iteraciones):
  #nombreFichero = "./static/mandelbrot.png"
  ruta="./static/"
  nombreFichero = f"mandel_x1{x1}y1{y1}x2{x2}y2{y2}ancho{ancho}.png"
  xa = x1
  xb = x2
  ya = y1
  yb = y2
  maxIt = iteraciones
  # image size
  imgx = ancho
  imgy = int(abs (y2 - y1) * ancho / abs(x2 - x1));

  im = Image.new('RGB', (imgx, imgy), color = 'black')

  for y in range(imgy):
    zy = y * (yb - ya) / (imgy - 1)  + ya

    for x in range(imgx):
      zx = x * (xb - xa) / (imgx - 1)  + xa
      z = zx + zy * 1j
      c = z

      for i in range(maxIt):
        if abs(z) > 2.0: break
        z = z * z + c

      i = maxIt - i

      col = (i%10*25, i%16*16, i%8*32)

      im.putpixel((x, y), col)

  im.save(ruta+nombreFichero);  # Grabamos en formato PNG
  return nombreFichero


#pintaMandelbrot(x1, y1, x2, y2, 400, 255, "fich.ppm");
