# Generated by Django 5.0.4 on 2024-04-26 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rtxapi', '0011_delete_userresults'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amberalert',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='amberalert',
            name='vehicle_LP',
            field=models.CharField(default='No Plate', max_length=100),
        ),
        migrations.AlterField(
            model_name='amberalert',
            name='vehicle_info',
            field=models.TextField(default=None),
        ),
    ]
