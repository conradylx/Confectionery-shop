# Generated by Django 3.1.2 on 2020-11-12 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_auto_20201112_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('K', 'Kruche'), ('S', 'Serniki'), ('D', 'Drożdżowe')], max_length=1),
        ),
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(choices=[('P', 'primary'), ('D', 'danger'), ('S', 'secondary')], max_length=1),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
