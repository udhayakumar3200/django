# Generated by Django 5.0.1 on 2024-02-12 09:48

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=250)),
                ('questionOptions', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=100), size=None)),
                ('answer', models.CharField(max_length=100)),
                ('created_At', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_At', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiz_name', models.CharField(max_length=100, null=True)),
                ('created_At', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_At', models.DateTimeField(auto_now_add=True, null=True)),
                ('questions', models.ManyToManyField(related_name='questions', to='quiz.question')),
            ],
        ),
    ]
