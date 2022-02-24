# Generated by Django 3.2.8 on 2021-10-26 17:25

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
            name='Instance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin', models.CharField(max_length=128)),
                ('name', models.CharField(max_length=128, unique=True)),
                ('stage', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('Student', 'Student'), ('Supervisor', 'Supervisor'), ('Admin', 'Admin'), ('Superadmin', 'Superadmin')], default='Student', max_length=10)),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='AllocationWebApp.instance')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('tags', models.TextField()),
                ('seSuitable', models.BooleanField(default=True)),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='AllocationWebApp.instance')),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='AllocationWebApp.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('preferenceNo', models.IntegerField(default=0)),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='AllocationWebApp.instance')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='AllocationWebApp.project')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='AllocationWebApp.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Allocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='AllocationWebApp.instance')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='AllocationWebApp.project')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='AllocationWebApp.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Algorithm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('size', models.IntegerField(default=0)),
                ('profile', models.CharField(max_length=128)),
                ('degree', models.IntegerField(default=0)),
                ('instance', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='AllocationWebApp.instance')),
            ],
        ),
    ]
