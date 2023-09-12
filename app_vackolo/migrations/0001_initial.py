# Generated by Django 4.0.3 on 2023-08-01 19:47

import app_vackolo.models
from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Allat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faj', models.CharField(choices=[('kutya', 'kutya'), ('cica', 'cica'), ('egyeb', 'egyéb')], default='kutya', max_length=200, verbose_name='kutya/cica')),
                ('meret', models.CharField(choices=[('kicsi', 'kistestű'), ('kozepes', 'közepes testű'), ('nagy', 'nagytestű')], default='kicsi', max_length=200, verbose_name='méret')),
                ('ivar', models.CharField(choices=[('fiu', 'fiú'), ('lany', 'lány')], default='fiu', max_length=200, verbose_name='ivar')),
                ('nev', models.CharField(max_length=200, verbose_name='név')),
                ('bekerulesideje', models.DateField()),
                ('szuletesiideje', models.DateField()),
                ('ivartalanitva', models.BooleanField()),
                ('eletkor', models.IntegerField(blank=True, editable=False, null=True)),
                ('virtualisgazdi', models.TextField(default='nincs')),
                ('orokbeadva', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
            bases=(parler.models.TranslatableModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='AllatMainImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='app_menhely/img/photos/', verbose_name='kiemelt kép')),
                ('photo_tumb', models.ImageField(editable=False, upload_to='app_menhely/img/thumbs/')),
                ('allat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_vackolo.allat')),
            ],
            bases=(app_vackolo.models.ImageHandlerMixin, models.Model),
        ),
        migrations.CreateModel(
            name='AllatImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='app_menhely/img/photos/', verbose_name='galéria kép')),
                ('photo_tumb', models.ImageField(editable=False, upload_to='app_menhely/img/thumbs/')),
                ('allat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_vackolo.allat')),
            ],
            bases=(app_vackolo.models.ImageHandlerMixin, models.Model),
        ),
        migrations.CreateModel(
            name='AllatTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('leiras', models.TextField(default='Leírás később érkezik. Amennyiben a képek alapján érdeklődnél, keress facebook messengeren vagy telefonon.')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='app_vackolo.allat')),
            ],
            options={
                'verbose_name': 'allat Translation',
                'db_table': 'app_vackolo_allat_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatedFieldsModelMixin, models.Model),
        ),
    ]
