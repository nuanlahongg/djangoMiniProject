# Generated by Django 4.1.7 on 2023-02-25 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProfileApp', '0010_savejobdetails_samplesale'),
    ]

    operations = [
        migrations.AddField(
            model_name='savejob',
            name='status',
            field=models.CharField(default='', max_length=1),
        ),
    ]
