# Generated by Django 3.0.2 on 2020-07-21 06:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pharmacy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('pharmacist', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DrugSupply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('drugName', models.CharField(max_length=200)),
                ('supplier', models.CharField(max_length=200)),
                ('number', models.IntegerField()),
                ('pharmacy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmacy.Pharmacy')),
            ],
            options={
                'unique_together': {('drugName', 'supplier')},
            },
        ),
    ]
