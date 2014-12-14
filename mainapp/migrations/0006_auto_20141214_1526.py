# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0005_question_selection_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedbackmessages',
            name='user',
            field=models.ForeignKey(default=None, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='feedbackmessages',
            name='version',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
