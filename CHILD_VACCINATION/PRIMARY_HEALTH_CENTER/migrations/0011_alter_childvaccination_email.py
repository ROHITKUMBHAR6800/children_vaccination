# Generated by Django 5.0.1 on 2024-03-11 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PRIMARY_HEALTH_CENTER', '0010_childvaccination_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='childvaccination',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]