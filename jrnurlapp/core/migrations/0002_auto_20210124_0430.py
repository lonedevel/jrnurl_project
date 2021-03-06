# Generated by Django 3.1.5 on 2021-01-24 04:30

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='URLCollection',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('collection_type', models.IntegerField(choices=[(100, 'Captured'), (200, 'Technical'), (300, 'News'), (400, 'Research'), (500, 'Games'), (600, 'Humor'), (900, 'Other')], default=100)),
                ('favorite', models.BooleanField(blank=True, null=True)),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=45), blank=True, null=True, size=25)),
            ],
            options={
                'verbose_name_plural': 'URL Collections',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='URLCollectionItems',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.urlcollection')),
            ],
            options={
                'verbose_name_plural': 'URL Collection Items',
            },
        ),
        migrations.CreateModel(
            name='URLItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField(max_length=2048)),
                ('visits', models.IntegerField()),
                ('created', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('modified', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=45), blank=True, null=True, size=None)),
                ('collection', models.ManyToManyField(through='core.URLCollectionItems', to='core.URLCollection')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'URL Items',
                'ordering': ['title'],
            },
        ),
        migrations.AddField(
            model_name='urlcollectionitems',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.urlitem'),
        ),
        migrations.AddField(
            model_name='urlcollectionitems',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='urlcollection',
            name='items',
            field=models.ManyToManyField(through='core.URLCollectionItems', to='core.URLItem'),
        ),
        migrations.AddField(
            model_name='urlcollection',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
