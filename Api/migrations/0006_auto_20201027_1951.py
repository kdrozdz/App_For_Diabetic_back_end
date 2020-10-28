# Generated by Django 3.0.7 on 2020-10-27 18:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Api', '0005_auto_20201027_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cooperate',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='cooperate', to=settings.AUTH_USER_MODEL),
        ),
    ]
