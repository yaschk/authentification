# Generated by Django 2.2.3 on 2019-07-18 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='last_name',
        ),
        migrations.AddField(
            model_name='customuser',
            name='email_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='first_and_last_name',
            field=models.CharField(blank=True, max_length=50, verbose_name='name'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='phone_confirmed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='unconfirmed_email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='unconfirmed email address'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='unconfirmed_phone',
            field=models.BooleanField(default=False),
        ),
    ]