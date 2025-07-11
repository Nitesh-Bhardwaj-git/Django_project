# Generated by Django 5.2.4 on 2025-07-04 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Expense_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='category',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='expense',
            name='type',
            field=models.CharField(choices=[('income', 'Income'), ('expense', 'Expense')], default='expense', max_length=7),
        ),
    ]
