""" Captcha.Visual.BAse

Base classes for visual CAPTCHAs. We use the Python Imaging Library
to manipulate these images.
"""
#
# PyCAPTCHA Package
# Copyright (C) 2004 Micah Dowty <micah@navi.cx>
#

import Captcha
import Image

__all__ = ['ImageCaptcha', 'Layer']


class ImageCaptcha(Captcha.BaseCaptcha):
    """Base class for image-based CAPTCHA tests.
       The render() function generates the CAPTCHA image at the given size by
       combining Layer instances from self.layers, which should be created by
       the subclass-defined getLayers().
       """
    defaultSize = (256,96)

    def __init__(self, *args, **kwargs):
        Captcha.BaseCaptcha.__init__(self)
        self._layers = self.getLayers(*args, **kwargs)

    def getImage(self):
        """Get a PIL image representing this CAPTCHA test, creating it if necessary"""
        if not self._image:
            self._image = self.render()
        return self._image

    def getLayers(self):
        """Subclasses must override this to return a list of Layer instances to render.
           Lists within the list of layers are recursively rendered.
           """
        return []

    def render(self, size=None):
        """Render this CAPTCHA, returning a PIL image"""
        if size is None:
            size = self.defaultSize
        img = Image.new("RGB", size)
        return self._renderList(self._layers, Image.new("RGB", size))

    def _renderList(self, l, img):
        for i in l:
            if type(i) == tuple or type(i) == list:
                img = self._renderList(i, img)
            else:
                img = i.render(img) or img
        return img


class Layer(object):
    """A renderable object representing part of a CAPTCHA.
       The render() function should return approximately the same result, regardless
       of the image size. This means any randomization must occur in the constructor.

       If the render() function returns something non-None, it is taken as an image to
       replace the current image with. This can be used to implement transformations
       that result in a separate image without having to copy the results back to the first.
       """
    def render(self, img):
        pass

### The End ###
