# Generated by Django 3.0.7 on 2020-10-27 18:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Api', '0002_auto_20201027_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cooperate',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='doctor_cooperate', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='cooperate',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='patient_cooperate', to=settings.AUTH_USER_MODEL),
        ),
    ]