# Generated by Django 4.2.1 on 2023-06-06 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0007_alter_landload_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='officebooking',
            name='status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('PAID', 'PAID')], default='PENDING', max_length=100),
        ),
    ]
