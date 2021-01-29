# Generated by Django 3.1.5 on 2021-01-28 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210128_0315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urlcollection',
            name='items',
            field=models.ManyToManyField(blank=True, through='core.URLCollectionItems', to='core.URLItem'),
        ),
        migrations.AlterField(
            model_name='urlitem',
            name='collection',
            field=models.ManyToManyField(blank=True, through='core.URLCollectionItems', to='core.URLCollection'),
        ),
    ]