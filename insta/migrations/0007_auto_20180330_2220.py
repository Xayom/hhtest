# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-30 22:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insta', '0006_auto_20180305_1430'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, max_length=255, verbose_name='Заголовок')),
                ('video', models.FileField(upload_to='videos/', verbose_name='Видосик')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='post',
            name='url',
        ),
        migrations.AlterField(
            model_name='post',
            name='img',
            field=models.FileField(upload_to='documents/', verbose_name='Фоточка'),
        ),
    ]