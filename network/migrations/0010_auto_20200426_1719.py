# Generated by Django 3.0.3 on 2020-04-26 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_auto_20200426_1659'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='programs',
            field=models.ManyToManyField(blank=True, default=None, related_name='schoolprograms', to='network.Program'),
        ),
    ]
