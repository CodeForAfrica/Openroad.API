from __future__ import absolute_import, unicode_literals
from django.http import HttpResponse
from django.conf import settings
from celery import task
from .models import Inbox
#from datetime import *

import requests
import datetime

@task()
def push_to_rapidpro():
    print("Task started")
    # Get unProcessed messages
    unprocessed_messages = Inbox.objects.filter(processed=0)[:1]

    #print ("Time : " + datetime.datetime.now().isoformat())
    #print "\n"
    #print ("Time #2 : " + datetime.datetime.utcnow().isoformat() + 'Z')

    if len(unprocessed_messages):
        message = unprocessed_messages[0]
        print(len(unprocessed_messages))
        message.processed = 1
        message.processed_at = datetime.datetime.now()
        message.save()

        print(message)
        payload = {
            'from': message.sender, 
            'text': message.body
            #'date': datetime.datetime.utcnow().isoformat() + 'Z'
        }
        print(payload)

        headers = {u'content-type': u'application/x-www-form-urlencoded'}
        rapidpro_request = requests.post(settings.RAPIDPRO_URL, data=payload, headers=headers)

        print(rapidpro_request)

        # Dummy request
        payload = {
            'from': '255711111111', 
            'text': 'Nothing'
            #'date': datetime.datetime.utcnow().isoformat() + 'Z'
        }
        print(payload)

        headers = {u'content-type': u'application/x-www-form-urlencoded'}
        rapidpro_request = requests.post(settings.RAPIDPRO_URL, data=payload, headers=headers)
        
        print(rapidpro_request)
            
        print(message)
        
    return 0