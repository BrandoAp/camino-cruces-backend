# Generated by Django 5.2.4 on 2025-07-24 09:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrovisita',
            name='hora_entrada',
            field=models.TimeField(auto_now_add=True, default=datetime.time(9, 58, 33, 663418)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usuario',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
