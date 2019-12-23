#!/usr/bin/env python
import sys
import os.path

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))

from base.settings import execute

if __name__ == "__main__":
    execute('fastor.base')

