# Generated by Django 4.1.3 on 2023-01-04 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appliWNR', '0002_alter_utilisateur_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]