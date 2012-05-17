#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# wikiquoter.py - Extrae citas directas para es.wikiquote.org
# Copyright (C) 2012 Pablo Castellano <pablo@anche.no>
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

# http://www.abc.es/20120413/sociedad/abci-wert-consejo-ministros-201204131341.html
# http://www.publico.es/espana/423455/wert-la-victoria-del-pp-no-fue-solo-por-mayoria-absoluta-sino-universal
# http://www.eleconomista.es/noticias/noticias/3780127/02/12/WertNo-estamos-para-gastar-40000-millones-de-euros-en-estudiantes-que-dejan-la-carrera-amedias.html
# http://www.cadenaser.com/sociedad/audios/wert-fuera-opositor-estaria-dando-saltos-alegria-han-restituido-temario-llevo-trabajando-anos/csrcsrpor/20120208csrcsrsoc_8/Aes/ #no viene fecha?
# http://www.europapress.es/economia/noticia-alonso-pp-advierte-sindicatos-manifestaciones-no-crean-empleos-les-invita-trabajar-serio-20120211141205.htm
# http://www.lasprovincias.es/20120516/mas-actualidad/politica/corts-financiacion-local-201205161333.html
# http://www.elcorreo.com/vizcaya/20120516/local/azkuna-comercio-tiene-espabilar-201205161922.html

__author__ = "Pablo Castellano <pablo@anche.no>"
__license__ = "GNU GPLv3+"
__version__ = 0.6
__date__ = "17/05/2012 #caixarolada day!"


SUPPORTED_SITES = {'abc':'Diario ABC', 'publico':'Diario Público', 'economista':'El Economista', 'cs':'Cadena Ser', 'ep':'Europa Press', 'lp':'Las Provincias', 'correo':'El Correo'}

import re
import sys
import urllib


def getCite(url, t):
	if t not in SUPPORTED_SITES.keys():
		print "Unsupported site. Please choose one from:"
		print SUPPORTED_SITES.keys()
		return

	if not (url.startswith("http://") or url.startswith("www")):
		print "URL looks wrong :?"
		sys.exit(1)

	f = urllib.urlopen(url)

	ll = f.read()
	f.close()

	if t == 'abc':
		titulo = re.search('<title>(.*)</title>', ll).group(1).decode('latin-1')
		fecha = re.search('<div class="date">D&iacute;a (.*)( - <span>|</div>)', ll).group(1)
	elif t == 'publico':
		titulo = re.search('<title>(.*)</title>', ll).group(1)
		fecha = re.search('<span class="fecha">(.*)</span>', ll).group(1)
#		fecha_act = re.search('Actualizado: <span class="fecha">(.*)</span>', ll).group(1)
	elif t == 'economista':
		titulo = re.search('<title>(.*)</title>', ll).group(1)
		try:
			fecha = re.search('<div class="f-fecha">(.*) -', ll).group(1)
		except:
			fecha = re.search('<small>EcoDiario.es \| (.*) - .*<span', ll).group(1)	
	elif t == 'cs':
		titulo = re.search('<title>(.*) \| Sonido', ll).group(1).decode('latin-1')
		if url.endswith('/'): # No viene la fecha!! :?
			fecha = url.split('/')[-3][:8]
		else:
			fecha = url.split('/')[-2][:8]
	elif t == 'ep':
		titulo = re.search('<title>\r\n\t(.*)\r\n</title>', ll).group(1).decode('latin-1')
		import HTMLParser
		htmlparser = HTMLParser.HTMLParser()
		titulo = htmlparser.unescape(titulo)
		fecha = url.split('/')[-1].split('-')[-1][:8]
	elif t == 'lp':
	#	titulo = re.search('<div class="mpdato">(.*)</div>', ll).group(1)
		titulo = re.search('<title>(.*)</title>', ll).group(1)[:-15]
		fecha = re.search('<div class="date">(.*) - <span>', ll).group(1)
	elif t == 'correo':
		titulo = re.search('<title>(.*)</title>', ll).group(1)[:-11]
		fecha = re.search('<div class="date">(.*) - <span>', ll).group(1)

	print "* \"-frase-\"\n** Fuente: [%s %s], %s, %s" %(url, titulo, SUPPORTED_SITES[t], fecha)


if __name__ == "__main__":
	
	print "Wikiquoter - Extrae citas directas para es.wikiquote.org"
	print "Copyright (C) 2011-2012 Pablo Castellano"
	print "This program comes with ABSOLUTELY NO WARRANTY."
	print "This is free software, and you are welcome to redistribute it under certain conditions."
	print
	
	# type = abc, publico
	if len(sys.argv) != 3:
		print "Usage: %s <URL> <type>" %sys.argv[0]
		sys.exit(0)
	
	getCite(sys.argv[1], sys.argv[2])
