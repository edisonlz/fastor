""" Captcha

This is the PyCAPTCHA package, a collection of Python modules
implementing CAPTCHAs: automated tests that humans should pass,
but current computer programs can't. These tests are often
used for security.

See  http://www.captcha.net for more information and examples.

This project was started because the CIA project, written in
Python, needed a CAPTCHA to automate its user creation process
safely. All existing implementations the author could find were
written in Java or for the .NET framework, so a simple Python
alternative was needed.
"""
#
# PyCAPTCHA Package
# Copyright (C) 2004 Micah Dowty <micah@navi.cx>
#

__version__ = "0.3-pre"


# Check the python version here before we proceed further
requiredPythonVersion = (2,2,1)
def checkVersion():
    import sys, string
    if sys.version_info < requiredPythonVersion:
        raise Exception("%s requires at least Python %s, found %s instead." % (
            name,
            string.join(map(str, requiredPythonVersion), "."),
            string.join(map(str, sys.version_info), ".")))
checkVersion()


# Convenience imports
from Base import *
import File
import Words

### The End ###
