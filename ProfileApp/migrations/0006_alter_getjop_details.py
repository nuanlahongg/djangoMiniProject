# Generated by Django 4.1.7 on 2023-02-24 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProfileApp', '0005_getjop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='getjop',
            name='details',
            field=models.CharField(default='', max_length=100),
        ),
    ]
