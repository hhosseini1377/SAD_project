# Generated by Django 3.0.5 on 2020-07-21 20:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0003_auto_20200721_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='delete_notifications',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='doctor.Doctor'),
        ),
    ]