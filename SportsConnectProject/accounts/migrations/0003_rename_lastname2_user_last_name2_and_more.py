# Generated by Django 5.0.7 on 2024-09-02 18:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_lastname1'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='lastname2',
            new_name='last_name2',
        ),
        migrations.RemoveField(
            model_name='user',
            name='lastname1',
        ),
    ]
