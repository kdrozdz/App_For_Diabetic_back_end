# Generated by Django 3.0.4 on 2020-04-07 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Api', '0006_auto_20200407_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_patient', to='Api.Patient'),
        ),
    ]
