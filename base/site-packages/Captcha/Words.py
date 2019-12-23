""" Captcha.Words

Utilities for managing word lists and finding random words
"""
#
# PyCAPTCHA Package
# Copyright (C) 2004 Micah Dowty <micah@navi.cx>
#

import random, os
import File


class WordList(object):
    """A class representing a word list read from disk lazily.
       Blank lines and comment lines starting with '#' are ignored.
       Any number of words per line may be used. The list can
       optionally ingore words not within a given length range.
       """
    def __init__(self, fileName, minLength=None, maxLength=None):
        self.words = None
        self.fileName = fileName
        self.minLength = minLength
        self.maxLength = maxLength

    def read(self):
        """Read words from disk"""
        f = open(os.path.join(File.dataDir, "words", self.fileName))

        self.words = []
        for line in f.xreadlines():
            line = line.strip()
            if not line:
                continue
            if line[0] == '#':
                continue
            for word in line.split():
                if self.minLength is not None and len(word) < self.minLength:
                    continue
                if self.maxLength is not None and len(word) > self.maxLength:
                    continue
                self.words.append(word)

    def pick(self):
        """Pick a random word from the list, reading it in if necessary"""
        if self.words is None:
            self.read()
        return random.choice(self.words)


# Define several shared word lists that are read from disk on demand
basic_english            = WordList("basic-english")
basic_english_restricted = WordList("basic-english", minLength=5, maxLength=8)

defaultWordList = basic_english_restricted

### The End ###
