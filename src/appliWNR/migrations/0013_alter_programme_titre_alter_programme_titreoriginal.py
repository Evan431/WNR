# Generated by Django 4.1.4 on 2023-01-25 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appliWNR', '0012_alter_programme_note_global'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programme',
            name='titre',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='programme',
            name='titreOriginal',
            field=models.CharField(max_length=200),
        ),
    ]
