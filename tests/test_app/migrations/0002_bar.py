# Generated by Django 5.1.1 on 2024-09-13 16:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('foo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_app.foo')),
            ],
        ),
    ]