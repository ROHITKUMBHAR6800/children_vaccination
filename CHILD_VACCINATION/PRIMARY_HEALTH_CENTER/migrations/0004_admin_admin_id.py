# Generated by Django 5.0.1 on 2024-03-06 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PRIMARY_HEALTH_CENTER', '0003_rename_contact_no_admin_mobile_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='admin',
            name='admin_id',
            field=models.CharField(default='admin001', max_length=100),
        ),
    ]