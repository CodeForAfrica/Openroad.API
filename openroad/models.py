from __future__ import unicode_literals

from django.db import models
import datetime
from django.utils import timezone

class Inbox(models.Model):
    class Meta:
        db_table = 'inbox'
        
    sender = models.CharField(max_length=30,blank=False,default='')
    body = models.TextField(default='')
    processed = models.IntegerField(default=0)
    processed_at = models.DateField(blank=True,null=True)
    created_at = models.DateField(default=timezone.now, blank=False)


class Outbox(models.Model):
    class Meta:
        db_table = 'outbox'
        
    receiver = models.CharField(max_length=30,blank=False,default='')
    body = models.TextField(default='')
    chat_found = models.IntegerField(blank=False,default=0)
    processed = models.IntegerField(default=0)
    processed_at = models.DateField(blank=True,null=True)
    created_at = models.DateField(default=timezone.now, blank=False)