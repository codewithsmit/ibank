# Generated by Django 3.0.4 on 2020-03-20 16:31

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('headbranch', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeadBranch_Transaction',
            fields=[
                ('hbranch_tra_id', models.AutoField(primary_key=True, serialize=False)),
                ('hbranch_tra_type', models.IntegerField()),
                ('hbranch_tra_amount', models.IntegerField()),
                ('hbranch_tra_time', models.DateTimeField(default=datetime.datetime.now)),
                ('hbranch_tra_branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='headbranch.Branch')),
            ],
        ),
    ]
