# Generated by Django 3.2.25 on 2024-06-03 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_web_app', '0002_auto_20240531_1433'),
    ]

    operations = [
        migrations.RenameField(
            model_name='computer',
            old_name='state_icon',
            new_name='icon',
        ),
    ]
