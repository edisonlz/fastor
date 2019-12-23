""" Captcha.Visual.Tests

Visual CAPTCHA tests
"""
#
# PyCAPTCHA Package
# Copyright (C) 2004 Micah Dowty <micah@navi.cx>
#

from Captcha.Visual import Text, Backgrounds, Distortions, ImageCaptcha
from Captcha import Words
import random

__all__ = ["PseudoGimpy", "AngryGimpy", "AntiSpam"]


class PseudoGimpy(ImageCaptcha):
    """A relatively easy CAPTCHA that's somewhat easy on the eyes"""
    def getLayers(self):
        word = Words.defaultWordList.pick()
        self.addSolution(word)
        return [
            random.choice([
                Backgrounds.CroppedImage(),
                Backgrounds.TiledImage(),
            ]),
            Text.TextLayer(word, borderSize=1),
            Distortions.SineWarp(),
            ]


class AngryGimpy(ImageCaptcha):
    """A harder but less visually pleasing CAPTCHA"""
    def getLayers(self):
        word = Words.defaultWordList.pick()
        self.addSolution(word)
        return [
            Backgrounds.TiledImage(),
            Backgrounds.RandomDots(),
            Text.TextLayer(word, borderSize=1),
            Distortions.WigglyBlocks(),
            ]


class AntiSpam(ImageCaptcha):
    """A fixed-solution CAPTCHA that can be used to hide email addresses or URLs from bots"""
    fontFactory = Text.FontFactory(20, "vera/VeraBd.ttf")
    defaultSize = (512,50)

    def getLayers(self, solution="murray@example.com"):
        self.addSolution(solution)

        textLayer = Text.TextLayer(solution,
                                   borderSize = 2,
                                   fontFactory = self.fontFactory)

        return [
            Backgrounds.CroppedImage(),
            textLayer,
            Distortions.SineWarp(amplitudeRange = (2, 4)),
            ]

### The End ###
