# Generated by Django 5.0.1 on 2024-04-03 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rtxapi', '0004_amberalert_active_alter_amberalert_alert_lat_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserResults',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UserID', models.CharField(max_length=100)),
                ('result_data', models.JSONField()),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='amberalert',
            options={},
        ),
    ]
