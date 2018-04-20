# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-24 05:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patentanalysis', '0004_phrase_field_analyze'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChemicalPhrase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=200)),
                ('count', models.IntegerField()),
                ('field_analyze', models.CharField(max_length=100)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patentanalysis.Collection')),
            ],
        ),
    ]
