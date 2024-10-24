# Generated by Django 5.0.1 on 2024-10-24 10:00

import chirps.models
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chirp',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('text', models.TextField(max_length=500, null=True)),
                ('chirped', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('chirper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChirpComment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('text', models.TextField(max_length=500)),
                ('sent', models.DateTimeField(auto_now_add=True)),
                ('chirp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chirps.chirp')),
                ('chirper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChirpLike',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('liked', models.DateTimeField(auto_now_add=True)),
                ('chirp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chirps.chirp')),
                ('chirper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ChirpMedia',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('media', models.FileField(blank=True, null=True, upload_to=chirps.models.media_directory_path)),
                ('media_url', models.URLField(blank=True, null=True)),
                ('caption', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('chirp', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='media', to='chirps.chirp')),
            ],
        ),
    ]
