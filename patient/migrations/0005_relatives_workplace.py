# Generated by Django 4.2.4 on 2023-10-06 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0004_relatives'),
    ]

    operations = [
        migrations.AddField(
            model_name='relatives',
            name='Workplace',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
