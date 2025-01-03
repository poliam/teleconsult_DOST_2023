# Generated by Django 4.2.7 on 2023-11-02 04:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0006_medicine_allergies'),
    ]

    operations = [
        migrations.CreateModel(
            name='global_psychotrauma_screen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('consultation_date', models.DateTimeField(auto_now_add=True)),
                ('event_description', models.TextField(blank=True, null=True)),
                ('event_happened', models.CharField(blank=True, max_length=250, null=True)),
                ('physical_violence', models.CharField(blank=True, max_length=250, null=True)),
                ('sexual_violence', models.CharField(blank=True, max_length=250, null=True)),
                ('emotional_abuse', models.CharField(blank=True, max_length=250, null=True)),
                ('serious_injury', models.CharField(blank=True, max_length=250, null=True)),
                ('life_threatening', models.CharField(blank=True, max_length=250, null=True)),
                ('sudden_death_of_loved_one', models.BooleanField(default=0)),
                ('cause_harm_to_others', models.BooleanField(default=0)),
                ('covid', models.BooleanField(default=0)),
                ('single_event_occurring', models.CharField(blank=True, max_length=250, null=True)),
                ('range_event_occurring_from', models.CharField(blank=True, max_length=250, null=True)),
                ('range_event_occurring_to', models.CharField(blank=True, max_length=250, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now_add=True)),
                ('history', models.TextField(blank=True, null=True)),
                ('status', models.BooleanField(default=1)),
                ('is_delete', models.BooleanField(default=0)),
                ('details', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='patient.details')),
            ],
        ),
        migrations.CreateModel(
            name='considering_event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('considering_event_1', models.BooleanField(default=0)),
                ('considering_event_2', models.BooleanField(default=0)),
                ('considering_event_3', models.BooleanField(default=0)),
                ('considering_event_4', models.BooleanField(default=0)),
                ('considering_event_5', models.BooleanField(default=0)),
                ('considering_event_6', models.BooleanField(default=0)),
                ('considering_event_7', models.BooleanField(default=0)),
                ('considering_event_8', models.BooleanField(default=0)),
                ('considering_event_9', models.BooleanField(default=0)),
                ('considering_event_10', models.BooleanField(default=0)),
                ('considering_event_11', models.BooleanField(default=0)),
                ('considering_event_12', models.BooleanField(default=0)),
                ('considering_event_13', models.BooleanField(default=0)),
                ('considering_event_14', models.BooleanField(default=0)),
                ('considering_event_15', models.BooleanField(default=0)),
                ('considering_event_16', models.BooleanField(default=0)),
                ('considering_event_17', models.BooleanField(default=0)),
                ('considering_event_18', models.BooleanField(default=0)),
                ('considering_event_19', models.BooleanField(default=0)),
                ('considering_event_20', models.BooleanField(default=0)),
                ('considering_event_21', models.BooleanField(default=0)),
                ('considering_event_22', models.BooleanField(default=0)),
                ('considering_event_23', models.CharField(blank=True, max_length=250, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now_add=True)),
                ('history', models.TextField(blank=True, null=True)),
                ('status', models.BooleanField(default=1)),
                ('is_delete', models.BooleanField(default=0)),
                ('global_psychotrauma_screen', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='patient.global_psychotrauma_screen')),
            ],
        ),
    ]
