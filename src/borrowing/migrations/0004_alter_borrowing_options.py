# Generated by Django 5.1.6 on 2025-03-01 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('borrowing', '0003_alter_borrowing_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='borrowing',
            options={'ordering': ['expected_return_date']},
        ),
    ]
