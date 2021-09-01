# Generated by Django 3.2.6 on 2021-09-01 00:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('schedulr', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='contact_phone',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='shift',
            name='company',
            field=models.ForeignKey(default='Company', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='shift_company', to='schedulr.company'),
        ),
        migrations.AlterField(
            model_name='shift',
            name='created_by',
            field=models.ForeignKey(default='Admin', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='shift_admin', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='shift',
            name='position',
            field=models.ForeignKey(default='Position', on_delete=django.db.models.deletion.SET_DEFAULT, related_name='shift_position', to='schedulr.position'),
        ),
        migrations.RemoveField(
            model_name='shift',
            name='staff_claimed',
        ),
        migrations.AddField(
            model_name='shift',
            name='staff_claimed',
            field=models.ManyToManyField(default='Worker', related_name='shift_claims', to=settings.AUTH_USER_MODEL),
        ),
    ]
