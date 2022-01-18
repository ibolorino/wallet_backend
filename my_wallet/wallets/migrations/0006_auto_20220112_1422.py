# Generated by Django 3.2.10 on 2022-01-12 14:22

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wallets', '0005_order_ordertype'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='asset',
            options={'verbose_name': 'Ativo'},
        ),
        migrations.AlterModelOptions(
            name='assettype',
            options={'verbose_name': 'Tipo de Ativo'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Ordem', 'verbose_name_plural': 'Ordens'},
        ),
        migrations.AlterModelOptions(
            name='ordertype',
            options={'verbose_name': 'Tipo de Ordem', 'verbose_name_plural': 'Tipo de Ordens'},
        ),
        migrations.AlterModelOptions(
            name='wallet',
            options={'verbose_name': 'Carteira'},
        ),
        migrations.AlterModelOptions(
            name='wallet_asset',
            options={'verbose_name': 'Carteira_Ativo'},
        ),
        migrations.AlterField(
            model_name='asset',
            name='asset_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallets.assettype', verbose_name='Tipo'),
        ),
        migrations.AlterField(
            model_name='asset',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='assettype',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='assettype',
            name='parent_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='wallets.assettype', verbose_name='Tipo'),
        ),
        migrations.AlterField(
            model_name='order',
            name='asset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallets.asset', verbose_name='Ativo'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_date',
            field=models.DateField(verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallets.ordertype', verbose_name='Tipo de Ordem'),
        ),
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.IntegerField(verbose_name='Quantidade'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_orders', to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
        migrations.AlterField(
            model_name='order',
            name='value',
            field=models.FloatField(verbose_name='Valor'),
        ),
        migrations.AlterField(
            model_name='ordertype',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='ordertype',
            name='short_name',
            field=models.CharField(max_length=5, verbose_name='Nome abreviado'),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='asset',
            field=models.ManyToManyField(blank=True, through='wallets.Wallet_Asset', to='wallets.Asset', verbose_name='Ativo'),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='update_date',
            field=models.DateField(default=datetime.datetime(2022, 1, 12, 14, 22, 38, 938362), verbose_name='Última atualização'),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuário'),
        ),
        migrations.AlterField(
            model_name='wallet_asset',
            name='asset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallets.asset', verbose_name='Ativo'),
        ),
        migrations.AlterField(
            model_name='wallet_asset',
            name='invested_amount',
            field=models.FloatField(default=0, verbose_name='Total investido'),
        ),
        migrations.AlterField(
            model_name='wallet_asset',
            name='quantity',
            field=models.IntegerField(default=0, verbose_name='Quantidade'),
        ),
        migrations.AlterField(
            model_name='wallet_asset',
            name='wallet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallets.wallet', verbose_name='Carteira'),
        ),
    ]
