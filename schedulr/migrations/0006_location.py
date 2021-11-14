# Generated by Django 3.2.7 on 2021-11-11 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedulr', '0005_auto_20211019_0217'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='null', max_length=200)),
                ('street', models.CharField(default='null', max_length=200)),
                ('city', models.CharField(default='null', max_length=100)),
                ('state', models.CharField(default='NA', max_length=2)),
                ('zip', models.CharField(default='null', max_length=5)),
                ('lat', models.CharField(default='null', max_length=100)),
                ('lng', models.CharField(default='null', max_length=100)),
            ],
        ),
    ]
