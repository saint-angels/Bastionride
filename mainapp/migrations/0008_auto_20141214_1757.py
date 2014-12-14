# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_auto_20141214_1733'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedbackmessages',
            name='version',
        ),
        migrations.AddField(
            model_name='feedbackmessages',
            name='previous_version',
            field=models.ForeignKey(default=None, to='mainapp.FeedbackMessages', null=True),
            preserve_default=True,
        ),
    ]
