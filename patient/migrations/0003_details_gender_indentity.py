# Generated by Django 4.2.4 on 2023-10-06 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0002_alter_details_bod'),
    ]

    operations = [
        migrations.AddField(
            model_name='details',
            name='gender_indentity',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
