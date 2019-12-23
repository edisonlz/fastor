# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# Author: Emanuel Fonseca
# Email:  emdfonseca<at>gmail<dot>com
# Date:   25 August 2008
#
# Author: Eugene Kin Chee Yip
# Date:   7 Nov 2008




##########################################
# title class
class title(dict):
	def __init__(self, title, style=None):
		self['text'] = title
		self.set_style(style)

	def set_style(self, style):
		self['style'] = style if style else '{color: #000000; font-size: 12px;}'

class y_legend(title):
	pass

class x_legend(title):
	pass

##########################################
# axis classes
class axis(dict):
	def __init__(self, stroke = None, colour = None, grid_colour = None, labels = None, max = None, min = None, steps = None, offset = None):
		self.set_stroke(stroke)
		self.set_colour(colour)
		self.set_grid_colour(grid_colour)
		self.set_labels(labels)
		self.set_steps(steps)
		self.set_offset(offset)
		self.set_max(max)
		self.set_min(min)

	def set_stroke(self, stroke):
		if stroke:
			self['stroke'] = stroke

	def set_colour(self, colour):
		if colour:
			self['colour'] = colour
    
	def set_grid_colour(self, grid_colour):
		if grid_colour:
			self['grid-colour'] = grid_colour

	def set_labels(self, labels):
		if labels:
			self['labels'] = labels

	def set_steps(self, steps):
		if steps:
			self['steps'] = steps
			
	def set_offset(self, offset):
		if offset is not None:
			self['offset'] = offset
			
	def set_max(self, max):
		if max:
			self['max'] = max

	def set_min(self, min):
		if min:
			self['min'] = min
			
class x_axis(axis):
	def __init__(self, stroke = None, tick_height = None, colour = None, grid_colour = None, labels = None, three_d = None, max = None, min = None, steps = None, offset = None):
		axis.__init__(self, stroke, colour, grid_colour, labels, max, min, steps, offset)
		self.set_tick_height(tick_height)
		self.set_3d(three_d)
		
	def set_tick_height(self, tick_height):
		if tick_height:
			self['tick-height'] = tick_height
		
	def set_3d(self, three_d):
		if three_d:
			self['3d'] = three_d

class y_axis(axis):
	def __init__(self, stroke = None, tick_length = None, colour = None, grid_colour = None, labels = None, max = None, min = None, steps = None, offset = None):
		axis.__init__(self, stroke, colour, grid_colour, labels, max, min, steps, offset)
		self.set_tick_length(tick_length)
		self.set_offset(offset)
		
	def set_tick_length(self, tick_length):
		if tick_length:
			self['tick-length'] = tick_length

class radar_axis(axis):
	def __init__(self, stroke = None, tick_height = None, colour = None, grid_colour = None, labels = None, max = None, min = None, steps = None, spoke_labels = None):
		axis.__init__(self, stroke, colour, grid_colour, labels, max, min, steps)
		self.set_tick_height(tick_height)
		self.set_spoke_labels(spoke_labels)

	def set_tick_height(self, tick_height):
		if tick_height:
			self['tick-height'] = tick_height
			
	def set_spoke_labels(self, spoke_labels):
		if spoke_labels:
			self['spoke-labels'] = {'labels': spoke_labels}


##########################################
# tooltip class
class tooltip(dict):
	def __init__(self, shadow = None, stroke = None, colour = None, bg_colour = None, title_style = None, body_style = None, behaviour = None):
		self.set_shadow(shadow)
		self.set_stroke(stroke)
		self.set_colour(colour)
		self.set_background(bg_colour)
		self.set_title(title_style)
		self.set_body(body_style)
		self.set_behaviour(behaviour)

	def set_shadow(self, shadow):
		if shadow is not None:
			self['shadow'] = shadow
    
	def set_stroke(self, stroke):
		if stroke:
			self['stroke'] = stroke
    
	def set_colour(self, colour):
		if colour:
			self['colour'] = colour
    
	def set_background(self, background):
		if background:
			self['background'] = background
    
	def set_title(self, title):
		if title:
			self['title'] = title
    
	def set_body(self, body):
		if body:
			self['body'] = body
			
	def set_behaviour(self, behaviour):
		if behaviour == 'proximity':
			self['mouse'] = 1
		if behaviour == 'hover':
			self['mouse'] = 2



