# Generated by Django 3.0.3 on 2020-04-26 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alternativeSuccess', '0007_auto_20200426_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='name',
            field=models.TextField(blank=True),
        ),
    ]
