# Generated by Django 5.0.6 on 2024-05-13 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_paymentsremitted_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessprofile',
            name='business_id',
            field=models.CharField(blank=True, max_length=355, null=True),
        ),
    ]
