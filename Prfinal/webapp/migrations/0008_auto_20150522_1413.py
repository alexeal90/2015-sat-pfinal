# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_auto_20150520_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='fondo',
            field=models.CharField(default=123, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='letra',
            field=models.CharField(default=1234, max_length=30),
            preserve_default=False,
        ),
    ]
