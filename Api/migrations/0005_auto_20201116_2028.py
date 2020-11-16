# Generated by Django 3.0.7 on 2020-11-16 19:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Api', '0004_auto_20201114_1504'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='food',
            name='for_every_one',
        ),
        migrations.AddField(
            model_name='food',
            name='units',
            field=models.IntegerField(choices=[(1, '100g'), (2, '10g'), (3, 'psc')], default=1),
        ),
        migrations.RemoveField(
            model_name='food',
            name='patient',
        ),
        migrations.AddField(
            model_name='food',
            name='patient',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='food', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
