# Generated by Django 3.2.7 on 2021-09-06 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedulr', '0003_auto_20210904_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='shift',
            name='billrate',
            field=models.CharField(default=0, max_length=10),
        ),
        migrations.AddField(
            model_name='shift',
            name='lat',
            field=models.CharField(default='null', max_length=100),
        ),
        migrations.AddField(
            model_name='shift',
            name='lng',
            field=models.CharField(default='null', max_length=100),
        ),
        migrations.AddField(
            model_name='shift',
            name='payrate',
            field=models.CharField(default=0, max_length=10),
        ),
    ]