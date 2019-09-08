# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Counter(models.Model):
    count = models.IntegerField(blank=False, default=0)

class Artist(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100)
    related = models.ManyToManyField("self", related_name="_related", symmetrical=False, blank=True)
