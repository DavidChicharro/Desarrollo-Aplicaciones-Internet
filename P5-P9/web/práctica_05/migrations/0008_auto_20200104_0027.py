# Generated by Django 2.2.6 on 2020-01-04 00:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('práctica_05', '0007_auto_20200104_0024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grupo',
            name='origen_grupo_lat',
        ),
        migrations.RemoveField(
            model_name='grupo',
            name='origen_grupo_long',
        ),
    ]
