# Generated by Django 4.2.16 on 2024-11-18 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eliminacionGauss', '0008_factlu_rglcramer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rglcramer',
            name='cramer_TermsIndp',
        ),
    ]
