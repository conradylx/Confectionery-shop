# Generated by Django 3.1.2 on 2020-11-12 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0051_auto_20201112_1958'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='c_name',
            new_name='name',
        ),
    ]
