# Generated by Django 4.2.16 on 2024-11-12 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eliminacionGauss', '0005_trnsmtx'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClcDeterm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cldt_Matrx', models.JSONField()),
                ('cldt_resultado', models.JSONField(blank=True, null=True)),
                ('cldt_ecuaciones', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='multMtrX',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mMrx_Matrx', models.JSONField()),
                ('mMrx_resultado', models.JSONField(blank=True, null=True)),
                ('mMrx_ecuaciones', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
