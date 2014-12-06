# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20141205_2346'),
    ]

    operations = [
        migrations.AddField(
            model_name='hits',
            name='browser',
            field=models.CharField(default=b'Unknown', max_length=40),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hits',
            name='os',
            field=models.CharField(default=b'Unknown', max_length=40),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hits',
            name='time',
            field=models.DateTimeField(),
        ),
    ]
