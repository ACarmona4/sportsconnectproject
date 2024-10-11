# Generated by Django 5.1.1 on 2024-10-11 03:05

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Facilities',
            fields=[
                ('idFacility', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='reservation/facilities/')),
            ],
        ),
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('time_slot', models.TimeField()),
                ('facilities', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='facility.facilities')),
            ],
            options={
                'unique_together': {('facilities', 'date', 'time_slot')},
            },
        ),
    ]
