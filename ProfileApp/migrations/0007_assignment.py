# Generated by Django 4.1.7 on 2023-02-24 09:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ProfileApp', '0006_alter_getjop_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('agid', models.CharField(default='', max_length=13, primary_key=True, serialize=False)),
                ('details', models.CharField(default='', max_length=100)),
                ('date', models.DateField(default=None)),
                ('getjop', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ProfileApp.getjop')),
                ('member', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='ProfileApp.member')),
            ],
        ),
    ]
