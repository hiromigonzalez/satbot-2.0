# Generated by Django 5.0.3 on 2024-04-09 07:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='documents', to='chat.course'),
        ),
    ]
