# Generated by Django 3.1.5 on 2021-01-28 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210124_0430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urlcollection',
            name='items',
            field=models.ManyToManyField(blank=True, null=True, through='core.URLCollectionItems', to='core.URLItem'),
        ),
        migrations.AlterField(
            model_name='urlitem',
            name='collection',
            field=models.ManyToManyField(blank=True, null=True, through='core.URLCollectionItems', to='core.URLCollection'),
        ),
    ]
