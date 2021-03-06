# Generated by Django 3.2.8 on 2021-11-14 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AllocationWebApp', '0003_alter_userprofile_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Csv',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.FileField(upload_to='csvs')),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
                ('activated', models.BooleanField(default=False)),
            ],
        ),
    ]
