# -*- coding: utf-8 -*-
"""
 Copyright 2005 Spike^ekipS <spikeekips@gmail.com>

	This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

"""
This is the derived work from,
--------------------------------------------------
	svgtopng - SVG to PNG converter
	Copyright (c) 2007 Guillaume Seguin <guillaume@segu.in>
	Licensed under GNU GPLv2
	From: http://guillaume.segu.in/blog/code/43/svg-to-png/
--------------------------------------------------

"""

import re, os
from image import ContentFile

try :
	import cairo, rsvg
except ImportError :
	class SVG (object) :
		def __init__ (self, cf) :
			self.cf = cf

		def render (self, *args, **kwargs) :
			raise
else :
	class SVG (object) :
		LIMIT_SVG_WIDTH = 2000
		LIMIT_SVG_HEIGHT = 5000

		def __init__ (self, cf) :
			self.cf = cf
			self.svg = rsvg.Handle(file=self.cf.name)

		def set_dimensions (self, width=None, height=None) :
			try : width = int(width)
			except : width = None

			try : height = int(height)
			except : height = None

			if width is None and height is None :
				width = self.svg.props.width
				height = self.svg.props.height
			elif width is not None :
				ratio = float(width) / self.svg.props.width
				height = int(ratio * self.svg.props.height)
			elif height is not None :
				ratio = float(height) / self.svg.props.height
				width = int(ratio * self.svg.props.width)

			if width > self.LIMIT_SVG_WIDTH or height > self.LIMIT_SVG_HEIGHT :
				width = self.svg.props.width
				height = self.svg.props.height

			return (width, height, )

		def __render (self, outputtype="png", width=None, height=None, ) :
			output = ContentFile("", name="%s.%s" % (self.cf.name, outputtype, ) )

			width, height, = self.set_dimensions(width, height)

			if outputtype == "pdf" :
				self.surface = cairo.PDFSurface(output, width, height, )
			elif outputtype == "ps" :
				self.surface = cairo.PSSurface(output, width, height, )
			elif outputtype == "png" :
				self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
			else :
				raise Exception, "Must set the 'outputtype'."

			cr = cairo.Context(self.surface)

			wscale = float(width) / self.svg.props.width
			hscale = float(height) / self.svg.props.height

			cr.scale(wscale, hscale)

			# create cairo
			self.svg.render_cairo(cr)

			if outputtype == "png" :
				self.surface.write_to_png(output)

			return output

		def render (self, width=None, height=None, outputtype=None, filename=None) :
			"""
			output, io is String.StringIO object.
			"""
			if outputtype is None and filename.strip() :
				ext = os.path.splitext(filename)[-1]
				if ext.startswith(".") :
					outputtype = re.compile("^\.").sub("", ext)

			tmp = self.__render(
				outputtype=outputtype,
				width=width,
				height=height,
			)

			tmp.seek(0)
			return tmp

if __name__ == "__main__" :
	import sys

	k = "test/1.png"
	width = 600
	height = None

	f = "test/tiger.svg"

	s = SVG(f)
	o = s.render(width=600, filename=k)

	sys.exit()

"""
Description
-----------


ChangeLog
---------


Usage
-----


"""

__author__ =  "Spike^ekipS <spikeekips@gmail.com>"

