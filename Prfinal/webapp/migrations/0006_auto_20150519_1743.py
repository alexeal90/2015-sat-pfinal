# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0005_auto_20150519_1627'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actividade',
            name='id_act',
        ),
        migrations.AddField(
            model_name='actividade',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, default=123, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
