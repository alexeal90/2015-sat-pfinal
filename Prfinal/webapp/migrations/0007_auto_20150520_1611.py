# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0006_auto_20150519_1743'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='id',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='password',
        ),
        migrations.AddField(
            model_name='usuario',
            name='actividades',
            field=models.ManyToManyField(to='webapp.Actividade'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usuario',
            name='event',
            field=models.CharField(default=1234, max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usuario',
            name='name',
            field=models.CharField(max_length=30, serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
