# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-12-07 06:50
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment_Details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_details', models.CharField(blank=True, max_length=64, null=True)),
                ('cheque_details', models.CharField(blank=True, max_length=64, null=True)),
                ('upload_image', models.FileField(blank=True, null=True, upload_to=users.models.image_upload_path)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.CharField(blank=True, max_length=64, null=True)),
                ('updated_date', models.DateTimeField(auto_now=True, null=True)),
                ('updated_by', models.CharField(blank=True, max_length=64, null=True)),
            ],
            options={
                'ordering': ['-pk'],
                'db_table': 'pm_Payment_Details',
            },
        ),
        migrations.RemoveField(
            model_name='project_details',
            name='payment_details',
        ),
        migrations.RemoveField(
            model_name='user',
            name='create_date',
        ),
        migrations.AlterModelTable(
            name='basic_assumptions',
            table='pm_basic_assumptions',
        ),
        migrations.AlterModelTable(
            name='project_details',
            table='pm_project_details',
        ),
        migrations.AlterModelTable(
            name='projectstatus',
            table='pm_project_status',
        ),
        migrations.AddField(
            model_name='payment_details',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='users.Project_Details'),
        ),
        migrations.AddField(
            model_name='payment_details',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
