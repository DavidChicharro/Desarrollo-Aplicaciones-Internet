# Generated by Django 2.2.6 on 2019-11-24 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('práctica_05', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='fecha_lanzamiento',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='grupo',
            name='fecha_fundacion',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='musico',
            name='fecha_nacimiento',
            field=models.DateField(blank=True, null=True),
        ),
    ]
