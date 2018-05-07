# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-03-01 00:03
from __future__ import unicode_literals

import build.models
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
            name='Alias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('alternate_id', models.CharField(max_length=100)),
                ('alternate_title', models.CharField(max_length=100)),
                ('comment', models.CharField(max_length=1000)),
            ],
            options={
                'verbose_name_plural': 'Aliases',
            },
        ),
        migrations.CreateModel(
            name='Bundle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('directory', models.CharField(default='Not Created', max_length=1000)),
                ('lid', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('status', models.CharField(choices=[('b', 'Build'), ('r', 'Review'), ('s', 'Submit')], default='b', max_length=1)),
                ('bundle_type', models.CharField(choices=[('Archive', 'Archive'), ('Supplemental', 'Supplemental')], default='Archive', max_length=12)),
                ('version', models.CharField(choices=[('1.7.0.0', '1.7.0.0'), ('1.8.0.0', '1.8.0.0'), ('1.9.0.0', '1.9.0.0')], default='1.8.0.0', max_length=7)),
                ('date_coordinates', models.DateField()),
                ('time_coordinates', models.TimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Calibrated',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('bundle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='build.Bundle')),
            ],
        ),
        migrations.CreateModel(
            name='Choice_Instruments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Citation_Information',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_list', models.CharField(help_text='Lastname, F. M.; ', max_length=100)),
                ('description', models.CharField(max_length=1000)),
                ('editor_list', models.CharField(help_text='Lastname, F. M.; ', max_length=100)),
                ('keyword', models.CharField(max_length=100)),
                ('publication_year', models.DateField()),
                ('bundle', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='build.Bundle')),
            ],
        ),
        migrations.CreateModel(
            name='Collections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_document', models.BooleanField(default=True)),
                ('has_context', models.BooleanField(default=True)),
                ('has_xml_schema', models.BooleanField(default=True)),
                ('has_data', models.BooleanField(default=False)),
                ('has_browse', models.BooleanField(default=False)),
                ('has_calibrated', models.BooleanField(default=False)),
                ('has_geometry', models.BooleanField(default=False)),
                ('bundle', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='build.Bundle')),
            ],
            options={
                'verbose_name_plural': 'Collections',
            },
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calibrated', models.BooleanField(default=False)),
                ('derived', models.BooleanField(default=False)),
                ('raw', models.BooleanField(default=False)),
                ('reduced', models.BooleanField(default=False)),
                ('bundle', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='build.Bundle')),
            ],
        ),
        migrations.CreateModel(
            name='Derived',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('bundle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='build.Bundle')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('directory', models.CharField(default='Not Created', max_length=1000)),
                ('label', models.CharField(max_length=1000)),
                ('lid', models.CharField(default='', max_length=255)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('title', models.CharField(max_length=100)),
                ('actual_document', models.FileField(upload_to=build.models.get_user_document_directory)),
                ('pds3_label', models.FileField(upload_to=build.models.get_user_document_directory)),
                ('bundle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='build.Bundle')),
            ],
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('lid', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=100)),
                ('type_of', models.CharField(max_length=20)),
                ('bundle', models.ManyToManyField(to='build.Bundle')),
            ],
        ),
        migrations.CreateModel(
            name='Instrument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('type_of', models.CharField(max_length=100)),
                ('lid', models.CharField(max_length=255)),
                ('raw_data', models.CharField(max_length=100)),
                ('bundle', models.ManyToManyField(blank=True, to='build.Bundle')),
            ],
        ),
        migrations.CreateModel(
            name='InstrumentHost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(choices=[('Laboratory', 'Laboratory'), ('Observatory', 'Observatory')], max_length=100)),
                ('type_of', models.CharField(max_length=100)),
                ('lid', models.CharField(max_length=255)),
                ('raw_data', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('bundle', models.ManyToManyField(to='build.Bundle')),
            ],
        ),
        migrations.CreateModel(
            name='Product_Bundle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('directory', models.CharField(default='Not Created', max_length=1000)),
                ('label', models.CharField(max_length=1000)),
                ('lid', models.CharField(max_length=255)),
                ('bundle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='build.Bundle')),
            ],
        ),
        migrations.CreateModel(
            name='Product_Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('directory', models.CharField(default='Not Created', max_length=1000)),
                ('label', models.CharField(max_length=1000)),
                ('lid', models.CharField(max_length=255)),
                ('category', models.CharField(max_length=20)),
                ('bundle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='build.Bundle')),
            ],
        ),
        migrations.CreateModel(
            name='Raw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('bundle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='build.Bundle')),
            ],
        ),
        migrations.CreateModel(
            name='Reduced',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('bundle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='build.Bundle')),
            ],
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('type_of', models.CharField(max_length=100)),
                ('lid', models.CharField(max_length=255)),
                ('raw_data', models.CharField(max_length=100)),
                ('bundle', models.ManyToManyField(blank=True, to='build.Bundle')),
                ('instrument_host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='build.InstrumentHost')),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('bundle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='build.Bundle')),
            ],
        ),
        migrations.AddField(
            model_name='instrumenthost',
            name='mission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='build.Mission'),
        ),
        migrations.AddField(
            model_name='instrument',
            name='instrument_host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='build.InstrumentHost'),
        ),
        migrations.AddField(
            model_name='choice_instruments',
            name='instrument',
            field=models.ManyToManyField(to='build.Instrument'),
        ),
        migrations.AddField(
            model_name='choice_instruments',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='alias',
            name='bundle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='build.Bundle'),
        ),
        migrations.AlterUniqueTogether(
            name='bundle',
            unique_together=set([('user', 'name')]),
        ),
    ]
