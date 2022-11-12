# Generated by Django 4.0.4 on 2022-08-17 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0002_transaction_is_approved_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankOption',
            fields=[
                ('key', models.CharField(max_length=100)),
                ('value', models.PositiveBigIntegerField(primary_key=True, serialize=False, unique=True)),
            ],
        ),
    ]