# Generated by Django 4.0.3 on 2024-02-20 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_vackolo', '0006_remove_kapcsolat_telefonszam'),
    ]

    operations = [
        migrations.AddField(
            model_name='kapcsolat',
            name='facebookmessengercim',
            field=models.CharField(default='', max_length=50),
        ),
    ]
