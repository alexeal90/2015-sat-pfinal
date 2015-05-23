# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_usuario_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actividades',
            fields=[
                ('id_act', models.CharField(max_length=30, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=30)),
                ('kind', models.CharField(max_length=30)),
                ('price', models.CharField(max_length=30)),
                ('date', models.CharField(max_length=30)),
                ('length', models.CharField(max_length=30)),
                ('toolong', models.CharField(max_length=30)),
                ('url', models.CharField(max_length=30)),
                ('start', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
