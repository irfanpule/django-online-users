# Generated by Django 4.2.11 on 2024-05-07 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('online_users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='onlineuseractivity',
            name='path',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='onlineuseractivity',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
