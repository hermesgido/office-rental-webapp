# Generated by Django 4.2.1 on 2023-05-20 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('office', '0002_office_description_office_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='office',
            name='is_available',
            field=models.BooleanField(default=False),
        ),
    ]
