# Generated by Django 5.0.1 on 2024-02-16 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0009_remove_useranswers_samp'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswers',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
    ]