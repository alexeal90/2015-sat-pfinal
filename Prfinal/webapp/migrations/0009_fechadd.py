# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0008_auto_20150522_1413'),
    ]

    operations = [
        migrations.CreateModel(
            name='FechAdd',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateTimeField()),
                ('actividad', models.ForeignKey(to='webapp.Actividade')),
                ('usuario', models.ForeignKey(to='webapp.Usuario')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
