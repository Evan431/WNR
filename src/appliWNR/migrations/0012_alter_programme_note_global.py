# Generated by Django 4.1.4 on 2023-01-20 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appliWNR', '0011_remove_plateforme_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programme',
            name='note_global',
            field=models.FloatField(null=True),
        ),
    ]
