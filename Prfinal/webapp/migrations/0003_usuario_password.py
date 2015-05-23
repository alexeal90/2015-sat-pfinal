# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0002_auto_20150518_1725'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='password',
            field=models.CharField(default=123, max_length=12),
            preserve_default=False,
        ),
    ]
