# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class TDR(models.Model):
    imsi = models.CharField(max_length=15)
    userAgent = models.CharField(max_length=255)

    def __str__(self):
        return self.imsi + "   " + self.userAgent

# Create your models here.
