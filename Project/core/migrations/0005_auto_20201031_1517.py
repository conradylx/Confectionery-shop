# Generated by Django 3.1.2 on 2020-10-31 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20201031_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='descr',
            field=models.TextField(default='Test description'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('D', 'Drożdżowe'), ('K', 'Kruche'), ('S', 'Serniki')], max_length=1),
        ),
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(choices=[('D', 'danger'), ('P', 'primary'), ('S', 'secondary')], max_length=1),
        ),
    ]