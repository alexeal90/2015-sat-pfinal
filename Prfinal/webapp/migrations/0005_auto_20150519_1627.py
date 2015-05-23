# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_actividades'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Actividades',
            new_name='Actividade',
        ),
    ]
