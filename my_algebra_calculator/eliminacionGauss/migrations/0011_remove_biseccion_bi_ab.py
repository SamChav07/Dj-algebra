# Generated by Django 4.2.16 on 2024-11-19 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eliminacionGauss', '0010_biseccion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='biseccion',
            name='bi_AB',
        ),
    ]
