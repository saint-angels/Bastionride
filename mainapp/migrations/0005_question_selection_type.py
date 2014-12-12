# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20141211_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='selection_type',
            field=models.CharField(default=b'radio', max_length=10, choices=[(b'radio', b'Radio button'), (b'dropdown', b'Drop-down list')]),
            preserve_default=True,
        ),
    ]
