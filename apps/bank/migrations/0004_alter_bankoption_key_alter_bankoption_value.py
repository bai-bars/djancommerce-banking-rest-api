# Generated by Django 4.0.4 on 2022-08-17 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0003_bankoption'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankoption',
            name='key',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='bankoption',
            name='value',
            field=models.PositiveBigIntegerField(),
        ),
    ]
