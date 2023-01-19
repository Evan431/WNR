# Generated by Django 4.1.4 on 2023-01-19 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appliWNR', '0009_remove_note_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plateforme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('logo', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='programme',
            name='listPlateforme',
            field=models.ManyToManyField(to='appliWNR.plateforme'),
        ),
    ]