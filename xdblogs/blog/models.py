# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
import uuid
import hashlib
from config import PASSWORD_SALT
from utils import hashers

class Author(models.Model):
    uid = models.UUIDField(primary_key=True,default=uuid.uuid4)
    name = models.CharField(max_length=50,blank=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(null=False,unique=True)
    is_active = models.BooleanField(default=True)
    website = models.URLField(blank=True)

    def __unicode__(self):
        return u'%s' % (self.name)

    #set_password
    def set_password(self,raw_password):
        if not raw_password:
            return None
        self.password = hashers.make_password(raw_password,self.email)
        self.save()

    #check_password
    def check_password(self,raw_password):
        return hashers.check_password(raw_password,self.password,self.email)



class Categorys(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return u'%s' % (self.name)

class Tags(models.Model):
    name = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % (self.name)

class Articles(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=100,blank=True)
    pub_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    content = models.TextField()
    author = models.ForeignKey(Author,null=False)
    categorys = models.ForeignKey('Categorys')
    tags = models.ManyToManyField(Tags,blank=True)
    is_active = models.BooleanField(default=True)

