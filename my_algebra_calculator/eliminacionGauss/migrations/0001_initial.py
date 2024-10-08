# Generated by Django 4.2.16 on 2024-10-08 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Elim_Gauss',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EG_matriz', models.JSONField()),
                ('EG_tabla_id', models.IntegerField(max_length=100)),
                ('EG_resultado', models.JSONField(blank=True, null=True)),
                ('EG_ecuaciones', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ope_combinadas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('OpV_NmVectores', models.IntegerField()),
                ('OpV_DmVectores', models.IntegerField()),
                ('OpV_valor', models.FloatField()),
            ],
            options={
                'unique_together': {('OpV_NmVectores', 'OpV_DmVectores')},
            },
        ),
        migrations.CreateModel(
            name='MltFC_vertical',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MfcY_NmVectorX', models.IntegerField()),
                ('MfcY_NmVectorY', models.IntegerField()),
                ('MfcY_valor', models.FloatField()),
            ],
            options={
                'unique_together': {('MfcY_NmVectorX', 'MfcY_NmVectorY')},
            },
        ),
        migrations.CreateModel(
            name='MltFC_horizontal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MfcX_NmVectorX', models.IntegerField()),
                ('MfcX_NmVectorY', models.IntegerField()),
                ('MfcX_valor', models.FloatField()),
            ],
            options={
                'unique_together': {('MfcX_NmVectorX', 'MfcX_NmVectorY')},
            },
        ),
    ]
