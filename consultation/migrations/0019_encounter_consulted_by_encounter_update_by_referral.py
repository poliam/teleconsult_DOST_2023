# Generated by Django 4.2.7 on 2023-12-18 11:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('consultation', '0018_remove_encounter_cconsultation_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='encounter',
            name='consulted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='encounter',
            name='update_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='update_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referred_to', models.CharField(blank=True, max_length=250, null=True)),
                ('referred_from', models.CharField(blank=True, max_length=250, null=True)),
                ('brief_summary', models.TextField(blank=True, null=True)),
                ('impression', models.TextField(blank=True, null=True)),
                ('reason_for_referral', models.TextField(blank=True, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now_add=True)),
                ('history', models.TextField(blank=True, null=True)),
                ('status', models.BooleanField(default=1)),
                ('is_delete', models.BooleanField(default=0)),
                ('create_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('encounter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='consultation.encounter')),
            ],
        ),
    ]