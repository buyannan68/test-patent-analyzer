# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Collection(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now=True)
    last_update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10)
    # classification = models.CharField(max_length=100)
    # industry = models.CharField(max_length=100)

class CollectionFile(models.Model):
    user = models.ForeignKey(User)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    filename = models.TextField(max_length=100)
    filepath = models.FileField(upload_to = 'upload/')
    upload_on = models.DateTimeField(auto_now=True)

class Publication(models.Model):
    pub_num = models.CharField(max_length=32)
    date = models.DateField()
    title_dwpi = models.TextField(max_length=2000)
    title = models.TextField(max_length=1000)
    assignee = models.TextField(max_length=500)
    inventor = models.TextField(max_length=1000)
    abstract_dwpi = models.TextField(max_length=5000)
    abstract = models.TextField(max_length=5000)
    pri_num = models.TextField(max_length=500)
    pri_date = models.TextField(max_length=500)
    inpadoc_fam = models.TextField(max_length=500)
    dwpi_fam = models.TextField(max_length=500)
    abstract_dwpi = models.TextField(max_length=5000)
    claim = models.TextField(max_length=5000)
    ipc_cur = models.TextField(max_length=5000)
    inpadoc_stus = models.TextField(max_length=500)
    abstract_dwpi_nov = models.TextField(max_length=5000)
    abstract_dwpi_use = models.TextField(max_length=5000)
    abstract_dwpi_adv = models.TextField(max_length=5000)

class PubColRel(models.Model):
	collection = models.ForeignKey(Collection)
	publication = models.ForeignKey(Publication)
	
class Model(models.Model):
	collection = models.ForeignKey(Collection)
	created_on = models.DateTimeField(auto_now=True)
	path = models.TextField(max_length=500)

class Phrase(models.Model):
    text = models.TextField(max_length=200)
    category = models.CharField(max_length=100)
    publication = models.ForeignKey(Publication)
    collection = models.ForeignKey(Collection)
    source = models.CharField(max_length=100)
    field_analyze = models.CharField(max_length=100)

class ChemicalPhrase(models.Model):
    text = models.TextField(max_length=200)
    count = models.IntegerField()
    collection = models.ForeignKey(Collection)
    collectionfile =  models.ForeignKey(CollectionFile)
    source = models.CharField(max_length=100)
    field_analyze = models.CharField(max_length=100)

