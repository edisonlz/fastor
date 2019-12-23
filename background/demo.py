# -*- coding: utf-8 -*-
import os
import sys
import time
import logging
import json
import urllib
import re


PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../..')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../../..')))

from base.settings import load_django_settings

load_django_settings('fastor.base', 'fastor.app')
from redis_model.queue import Worker
from app.iclass.models import *




def do_sync_worker(data):
    print "**Recieve data: ", data
    logging.error(data)
   



if __name__ == "__main__":

    worker = Worker("demo.async.send",support_brpop=False)
    try:
        worker.register(do_sync_worker)
        worker.start()
    except KeyboardInterrupt:
        worker.stop()
        print "exited cleanly"
        sys.exit(1)
    except Exception as e:
        logging.error(e)




