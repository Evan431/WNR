# Generated by Django 4.1.4 on 2023-01-25 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appliWNR', '0014_alter_compagnieproduction_nom_alter_genre_nom_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='nom',
            field=models.CharField(max_length=350),
        ),
    ]
