# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-11 16:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(verbose_name='Answer')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Is Correct?')),
            ],
            options={
                'verbose_name': 'Answer',
                'verbose_name_plural': 'Answers',
            },
        ),
        migrations.CreateModel(
            name='Manual',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manual', models.CharField(max_length=256, verbose_name='Manual')),
            ],
            options={
                'verbose_name': 'Manual',
                'verbose_name_plural': 'Manual',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('page', models.PositiveSmallIntegerField(verbose_name='Page')),
                ('question', models.TextField(verbose_name='Question')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=256, verbose_name='Subject')),
                ('manual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examapp.Manual', verbose_name='Manual')),
            ],
            options={
                'verbose_name': 'Subject',
                'verbose_name_plural': 'Subjects',
            },
        ),
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_model', models.CharField(max_length=256, verbose_name='Test Model')),
                ('questions', models.PositiveSmallIntegerField(verbose_name='Number of questions')),
            ],
            options={
                'verbose_name': 'Test Model Subject',
                'verbose_name_plural': 'Test Model Subjects',
            },
        ),
        migrations.CreateModel(
            name='TestModelSubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.PositiveSmallIntegerField(verbose_name='Weight')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examapp.Subject', verbose_name='Subject')),
                ('test_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examapp.TestModel', verbose_name='Test Model')),
            ],
            options={
                'verbose_name': 'Test Model Subject',
                'verbose_name_plural': 'Test Model Subjects',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examapp.Subject', verbose_name='Subject'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='examapp.Question', verbose_name='Question'),
        ),
    ]
