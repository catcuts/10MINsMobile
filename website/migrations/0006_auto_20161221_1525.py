# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-21 07:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_video_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_Banned',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_InvitedAuthor',
            field=models.BooleanField(default=False),
        ),
    ]
