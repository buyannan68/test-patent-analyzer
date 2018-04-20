# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-24 05:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patentanalysis', '0005_chemicalphrase'),
    ]

    operations = [
        migrations.AddField(
            model_name='chemicalphrase',
            name='collectionfile',
            field=models.ForeignKey(default=17, on_delete=django.db.models.deletion.CASCADE, to='patentanalysis.CollectionFile'),
            preserve_default=False,
        ),
    ]
