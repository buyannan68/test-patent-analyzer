# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-04 05:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CollectionFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.TextField(max_length=100)),
                ('filepath', models.FileField(upload_to='upload/')),
                ('upload_on', models.DateTimeField(auto_now=True)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patentanalysis.Collection')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_num', models.CharField(max_length=32)),
                ('date', models.DateField()),
                ('title_dwpi', models.TextField(max_length=2000)),
                ('title', models.TextField(max_length=1000)),
                ('assignee', models.TextField(max_length=500)),
                ('inventor', models.TextField(max_length=1000)),
                ('abstract', models.TextField(max_length=5000)),
                ('pri_num', models.TextField(max_length=500)),
                ('pri_date', models.TextField(max_length=500)),
                ('inpadoc_fam', models.TextField(max_length=500)),
                ('dwpi_fam', models.TextField(max_length=500)),
                ('abstract_dwpi', models.TextField(max_length=5000)),
                ('claim', models.TextField(max_length=5000)),
                ('ipc_cur', models.TextField(max_length=5000)),
                ('inpadoc_stus', models.TextField(max_length=500)),
                ('abstract_dwpi_nov', models.TextField(max_length=5000)),
                ('abstract_dwpi_use', models.TextField(max_length=5000)),
                ('abstract_dwpi_adv', models.TextField(max_length=5000)),
            ],
        ),
    ]
