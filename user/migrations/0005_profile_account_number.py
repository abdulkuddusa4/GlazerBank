# Generated by Django 4.1.5 on 2023-02-07 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_profile_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='account_number',
            field=models.CharField(max_length=9, null=True),
        ),
    ]
