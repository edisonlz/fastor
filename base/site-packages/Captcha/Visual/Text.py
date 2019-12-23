""" Captcha.Visual.Text

Text generation for visual CAPTCHAs.
"""
#
# PyCAPTCHA Package
# Copyright (C) 2004 Micah Dowty <micah@navi.cx>
#

import random, os
from Captcha import Visual, File
import ImageFont, ImageDraw


class FontFactory(File.RandomFileFactory):
    """Picks random fonts and/or sizes from a given list.
       'sizes' can be a single size or a (min,max) tuple.
       If any of the given files are directories, all *.ttf found
       in that directory will be added.
       """
    extensions = [".ttf"]
    basePath = "fonts"

    def __init__(self, sizes, *fileNames):
        File.RandomFileFactory.__init__(self, *fileNames)

        if type(sizes) is tuple:
            self.minSize = sizes[0]
            self.maxSize = sizes[1]
        else:
            self.minSize = sizes
            self.maxSize = sizes

    def pick(self):
        """Returns a (fileName, size) tuple that can be passed to ImageFont.truetype()"""
        fileName = File.RandomFileFactory.pick(self)
        size = int(random.uniform(self.minSize, self.maxSize) + 0.5)
        return (fileName, size)

# Predefined font factories
defaultFontFactory = FontFactory((30, 40), "vera")


class TextLayer(Visual.Layer):
    """Represents a piece of text rendered within the image.
       Alignment is given such that (0,0) places the text in the
       top-left corner and (1,1) places it in the bottom-left.

       The font and alignment are optional, if not specified one is
       chosen randomly. If no font factory is specified, the default is used.
       """
    def __init__(self, text,
                 alignment   = None,
                 font        = None,
                 fontFactory = None,
                 textColor   = "black",
                 borderSize  = 0,
                 borderColor = "white",
                 ):
        if fontFactory is None:
            global defaultFontFactory
            fontFactory = defaultFontFactory

        if font is None:
            font = fontFactory.pick()

        if alignment is None:
            alignment = (random.uniform(0,1),
                         random.uniform(0,1))

        self.text        = text
        self.alignment   = alignment
        self.font        = font
        self.textColor   = textColor
        self.borderSize  = borderSize
        self.borderColor = borderColor

    def render(self, img):
        font = ImageFont.truetype(*self.font)
    	textSize = font.getsize(self.text)
        draw = ImageDraw.Draw(img)

        # Find the text's origin given our alignment and current image size
        x = int((img.size[0] - textSize[0] - self.borderSize*2) * self.alignment[0] + 0.5)
        y = int((img.size[1] - textSize[1] - self.borderSize*2) * self.alignment[1] + 0.5)

        # Draw the border if we need one. This is slow and ugly, but there doesn't
        # seem to be a better way with PIL.
        if self.borderSize > 0:
            for bx in (-1,0,1):
                for by in (-1,0,1):
                    if bx and by:
                        draw.text((x + bx * self.borderSize,
                                   y + by * self.borderSize),
                                  self.text, font=font, fill=self.borderColor)

        # And the text itself...
        draw.text((x,y), self.text, font=font, fill=self.textColor)

### The End ###
