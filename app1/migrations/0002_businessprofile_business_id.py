# Generated by Django 5.0.6 on 2024-05-13 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessprofile',
            name='business_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]