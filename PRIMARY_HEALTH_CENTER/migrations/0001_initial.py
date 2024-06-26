# Generated by Django 5.0.1 on 2024-03-06 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hospital_name', models.CharField(max_length=200)),
                ('mobile_no', models.CharField(max_length=13)),
                ('email', models.CharField(max_length=100)),
                ('area_add', models.CharField(max_length=200)),
                ('village_town', models.CharField(max_length=100)),
                ('pincode', models.CharField(max_length=10)),
                ('tehsil', models.CharField(max_length=100)),
                ('district', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
    ]
