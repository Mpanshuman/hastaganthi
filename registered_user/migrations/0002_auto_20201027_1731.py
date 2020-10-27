# Generated by Django 3.1.1 on 2020-10-27 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registered_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('phone', models.CharField(max_length=15, unique=True, verbose_name='mobile number')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='user_details',
            name='user',
        ),
        migrations.DeleteModel(
            name='Parents_Details',
        ),
        migrations.DeleteModel(
            name='User_Details',
        ),
    ]
