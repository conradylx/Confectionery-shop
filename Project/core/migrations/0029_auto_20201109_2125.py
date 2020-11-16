# Generated by Django 3.1.2 on 2020-11-09 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20201109_2122'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('K', 'Kruche'), ('D', 'Drożdżowe'), ('S', 'Serniki')], max_length=1),
        ),
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(choices=[('P', 'primary'), ('S', 'secondary'), ('D', 'danger')], max_length=1),
        ),
    ]
