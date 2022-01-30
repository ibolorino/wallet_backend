from statistics import quantiles
from django.db import models
from my_wallet.users.models import User
import datetime
from django.utils import timezone
from django.shortcuts import get_object_or_404
from services.google import *

class Asset(models.Model):
    name = models.CharField("Nome", max_length=255)
    ticker = models.CharField("Ticker", max_length=50)
    asset_type = models.ForeignKey("AssetType", verbose_name="Tipo", on_delete=models.CASCADE)
    sector = models.CharField("Setor", max_length=255, null=True, blank=True)
    cnpj = models.CharField("CNPJ", max_length=255, null=True, blank=True)
    current_price = models.FloatField("Preço Atual", null=True, blank=True)
    price_update_date = models.DateTimeField("Última Atualização", auto_now=False, auto_now_add=False, null=True, blank=True)

    class Meta():
        verbose_name = 'Ativo'

    def __str__(self):
        return f'{self.asset_type} - {self.name}'

    @staticmethod
    def update_all_prices():
        assets = Asset.objects.all()
        prices_sheet = GoogleSheeet(SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME)
        df = prices_sheet.to_dataframe()
        for asset in assets:
            try:
                asset.current_price = df.loc[df.ASSET == asset.ticker].iloc[0]['PRICE']
                asset.price_update_date = timezone.now()
                asset.save()
            except:
                continue


class AssetType(models.Model):
    name = models.CharField("Nome", max_length=255)
    parent_type = models.ForeignKey("AssetType", verbose_name="Tipo", on_delete=models.CASCADE, null=True, blank=True)

    class Meta():
        verbose_name = 'Tipo de Ativo'

    def __str__(self):
        return f'{self.name}'


class Wallet(models.Model):
    user = models.ForeignKey(User, verbose_name="Usuário", on_delete=models.CASCADE)
    update_date = models.DateField("Última atualização", auto_now=False, auto_now_add=False, default=datetime.datetime.now)
    asset = models.ManyToManyField("Asset", verbose_name="Ativo", through="Wallet_Asset", blank=True)

    class Meta():
        verbose_name = 'Carteira'

    def __str__(self):
        return f'{self.user}'

    def update_wallet(self, order):
        asset = order.asset
        quantity = order.quantity
        value = order.value
        order_type = order.order_type.short_name
        wallet_assets = Wallet_Asset.objects.filter(wallet=self, asset=asset)
        if wallet_assets.exists(): # atualiza wallet_asset
            wallet_asset = wallet_assets[0] 
        else: # cria wallet asset
            if order_type == 'V':
                return
            wallet_asset = Wallet_Asset.objects.create(wallet=self, asset=asset)
        if order_type == 'C':
            wallet_asset.quantity += quantity
            wallet_asset.invested_amount += value
        elif order_type == 'V':
            average_price = wallet_asset.invested_amount / wallet_asset.quantity
            wallet_asset.quantity -= quantity
            wallet_asset.invested_amount -= average_price * quantity
        wallet_asset.save()
        return


class Wallet_Asset(models.Model):
    wallet = models.ForeignKey("Wallet", verbose_name="Carteira", on_delete=models.CASCADE)
    asset = models.ForeignKey("Asset", verbose_name="Ativo", on_delete=models.CASCADE, related_name="inserted_wallet")
    quantity = models.IntegerField("Quantidade", default=0)
    invested_amount = models.FloatField("Total investido", default=0)

    class Meta():
        verbose_name = 'Carteira_Ativo'

    def __str__(self):
        return f'{self.wallet} - {self.asset}'

    @property
    def average_price(self):
        if self.quantity != 0:
            return self.invested_amount/self.quantity
        return 0

    @property
    def current_value(self):
        try:
            return self.quantity * self.asset.current_price
        except:
            return '-'

    def delete_order(self, order):
        signal_parameter = -1 if order.order_type == OrderType.buy_order() else 1
        if order.order_type == OrderType.buy_order():
            self.quantity -= order.quantity
            self.invested_amount -= order.value
        elif order.order_type == OrderType.sell_order():
            average_price = self.average_price
            self.quantity += order.quantity
            self.invested_amount += average_price * order.quantity
        self.save()
    
    def update_wallet(self, order, retrieve=False):
        if retrieve == True:
            pass
        else:
            if order.order_type == OrderType.buy_order():
                self.quantity += order.quantity
                self.invested_amount += order.value
            elif order.order_type == OrderType.sell_order():
                average_price = self.average_price
                self.quantity -= order.quantity
                self.invested_amount -= average_price * order.quantity
        return

    def calculate(self):
        orders = Order.objects.filter(asset=self.asset, user=self.wallet__user)
        quantity = 0
        for order in orders:
            quantity = quantity + order.quantity if order.order_type == OrderType.by_order() else quantity - order.quantity
        pass


class OrderType(models.Model):
    name = models.CharField("Nome", max_length=255)
    short_name = models.CharField("Nome abreviado", max_length=5)

    class Meta():
        verbose_name = 'Tipo de Ordem'
        verbose_name_plural = 'Tipo de Ordens'

    def __str__(self):
        return f'{self.short_name}'

    @staticmethod
    def buy_order():
        return get_object_or_404(OrderType, short_name='C')

    @staticmethod
    def sell_order():
        return get_object_or_404(OrderType, short_name='V')


class Order(models.Model):
    user = models.ForeignKey(User, verbose_name="Usuário", on_delete=models.CASCADE, related_name="user_orders")
    asset = models.ForeignKey("Asset", verbose_name="Ativo", on_delete=models.CASCADE)
    order_type = models.ForeignKey("OrderType", verbose_name="Tipo de Ordem", on_delete=models.CASCADE)
    order_date = models.DateField("Data", auto_now=False, auto_now_add=False)
    value = models.FloatField("Valor")
    quantity = models.IntegerField("Quantidade")

    class Meta():
        verbose_name = 'Ordem'
        verbose_name_plural = 'Ordens'

    def __str__(self):
        return f'{self.user} - {self.order_type} - {self.asset.ticker}'

    def create_wallet(self):
        wallet = Wallet.objects.create(user=self.user)
        wallet_asset = Wallet_Asset.objects.create(wallet=wallet, asset=self.asset, quantity=self.quantity, invested_amount=self.value)
        return wallet_asset