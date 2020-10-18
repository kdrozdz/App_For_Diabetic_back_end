# Generated by Django 3.0.7 on 2020-10-18 09:31

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
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Sugar_level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('without_a_meal', models.BooleanField(default=False)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='patient', to=settings.AUTH_USER_MODEL)),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='patient', to='Api.Doctor')),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_new', models.BooleanField(default=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('msg', models.TextField()),
                ('reciver', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_reciver_email', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_sender_email', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cooperate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accept_sender', models.BooleanField(default=False)),
                ('accept_reciver', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('rejected', models.BooleanField(default=False)),
                ('reciver', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_reciver_cooperate', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='user_sender_cooperate', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
