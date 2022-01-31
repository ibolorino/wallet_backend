# Generated by Django 3.2.10 on 2022-01-30 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0002_auto_20220127_0350'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='current_price',
            field=models.FloatField(blank=True, null=True, verbose_name='Preço Atual'),
        ),
        migrations.AddField(
            model_name='asset',
            name='price_update_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Última Atualização'),
        ),
    ]