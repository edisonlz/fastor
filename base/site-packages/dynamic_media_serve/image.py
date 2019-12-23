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

import urllib, os
from StringIO import StringIO

class ContentFile (StringIO) :

	def __init__ (self, content, name=None) :
		StringIO.__init__(self, content)
		self.name = name

	def read (self, size=None) :
		o = StringIO.read(self, size)

		if not size :
			self.seek(0)

		return o

try :
	import Image
except ImportError :
	def resize_image (*args, **kwargs) :
		return open(args[0], "rb").read()
else :
	def get_image_offset_sooa (size_orig, size_new, direction="center") :
		(w, h, ) = size_orig
		(w_new, h_new, ) = size_new

		# get image size ratio
		__pos = (0, 0, w_new, h_new, )

		if w > h : # resize height.
			__ratio = float(h_new) / float(h)
			h = h_new
			w = w * __ratio

			if direction == "topleft" :
				__offset_x0 = 0
				__offset_x1 = w_new
			else :
				if w > w_new :
					__offset_x0 = int(float(w - w_new) / float(2))
					__offset_x1 = int(w - float(w - w_new) / float(2))
				else :
					__offset_x0 = 0
					__offset_x1 = int(w)

			__pos = (
				__offset_x0,
				0,
				__offset_x1,
				int(h),
			)
		elif h > w : # resize width
			__ratio = float(w_new) / float(w)
			w = w_new
			h = h * __ratio

			if direction == "topleft" :
				__offset_y0 = 0
				__offset_y1 = h_new
			else :
				if h > h_new :
					__offset_y0 = int(float(h - h_new) / float(2))
					__offset_y1 = int(h - float(h - h_new) / float(2))
				else :
					__offset_y0 = 0
					__offset_y1 = h

			__pos = (
				0,
				__offset_y0,
				int(w),
				__offset_y1,
			)
		else : # height == width
			__offset_x0 = (w / 2) - (w_new / 2)
			__offset_x1 = __offset_x0 + w_new

			__offset_y0 = (h / 2) - (h_new / 2)
			__offset_y1 = __offset_y0 + h_new

			__pos = (
				__offset_x0,
				__offset_y0,
				__offset_x1,
				__offset_y1,
			)

		return ((int(w), int(h), ), __pos, )

	def resize_image (cf, size=(200, 200), mode="ratio", direction="center", improve=False, ) :
		im = Image.open(cf)

		(w, h, ) = im.size

		w_new = size[0]
		h_new = size[1]

		if w_new > w and h_new > h :
			return cf

		if not w_new or not h_new :
			mode="ratio"

		if (w_new is not None or h_new is not None) and \
					mode in ("topleft", "topright", "bottomleft", "bottomright", ) :

			__w = (w_new < w) and w_new or w
			__h = (h_new < h) and h_new or h

			if mode == "topleft" :
				offset = (0, 0, __w, __h, )
			elif mode == "topright" :
				offset = (
					(w_new < w) and w - w_new or 0,
					0,
					((w_new < w) and w - w_new or 0) + __w,
					__h,
				)
			elif mode == "bottomleft" :
				offset = (
					0,
					(h_new < h) and h - h_new or 0,
					__w,
					((h_new < h) and h - h_new or 0) + __h,
				)
			elif mode == "bottomright" :
				offset = (
					(w_new < w) and w - w_new or 0,
					(h_new < h) and h - h_new or 0,
					((w_new < w) and w - w_new or 0) + __w,
					((h_new < h) and h - h_new or 0) + __h,
				)

			im = im.crop(offset)
		elif (w_new is not None or h_new is not None) and mode == "sooa" :
			((w, h, ), __pos, ) = get_image_offset_sooa(im.size, size, direction, )
			im = im.resize((w, h, ), Image.ANTIALIAS)
			im = im.crop(__pos)
		elif (w_new is not None or h_new is not None) and mode == "flickr" :
			if h_new and h > h_new :
				__ratio = float(h_new) / float(h)
				h = h_new
				w = w * __ratio

			# resizing
			im = im.resize((int(w), int(h), ), Image.ANTIALIAS)

			# center-focused crop
			if w > w_new :
				im = im.crop(
					(
						int(float(w - w_new) / float(2)),
						0,
						int(w - (float(w - w_new) / float(2))),
						h,
					)
				)
		else :
			if w_new and w > w_new :
				__ratio = float(w_new) / float(w)
				w = w_new
				h = h * __ratio

			if h_new and h > h_new :
				__ratio = float(h_new) / float(h)
				h = h_new
				w = w * __ratio

			# resizing
			if improve :
				im = im.convert("RGB")
				cf.name += ".png"

			im = im.resize((int(w), int(h), ), Image.ANTIALIAS)

		try :
			if not os.path.splitext(cf.name)[1].strip() :
				cf.name += ".png"
		except :
			cf.name += ".png"

		tmp = ContentFile("", name=cf.name)
		try :
			im.save(tmp, **im.info)
		except KeyError, e :
			return cf

		tmp.seek(0)
		return tmp



"""
Description
-----------


ChangeLog
---------


Usage
-----


"""

__author__ =  "Spike^ekipS <spikeekips@gmail.com>"

