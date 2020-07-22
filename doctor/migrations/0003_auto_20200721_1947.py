# Generated by Django 3.0.5 on 2020-07-21 19:47

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0001_initial'),
        ('doctor', '0002_delete_notifications'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delete_notifications',
            name='reservation',
        ),
        migrations.AddField(
            model_name='delete_notifications',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='delete_notifications',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='patient.Patient'),
        ),
    ]
