# Generated by Django 4.1.4 on 2023-01-19 21:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appliWNR', '0010_plateforme_programme_listplateforme'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='plateforme',
            name='logo',
        ),
    ]
