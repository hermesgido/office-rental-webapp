# Generated by Django 4.2.1 on 2023-06-12 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0009_landload_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officebooking',
            name='status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('PAID', 'PAID'), ('CONTRACT OVER', 'CONTRACT OVER')], default='PENDING', max_length=100),
        ),
    ]
