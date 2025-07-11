# Generated by Django 5.2.3 on 2025-06-28 19:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Book_app', '0004_fine'),
    ]

    operations = [
        migrations.AddField(
            model_name='fine',
            name='member',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Book_app.member'),
        ),
        migrations.AlterField(
            model_name='fine',
            name='loan',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Book_app.loan'),
        ),
    ]
