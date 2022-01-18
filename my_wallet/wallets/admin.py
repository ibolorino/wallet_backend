from django.contrib import admin
from .models import Asset, AssetType, Wallet, Wallet_Asset, Order, OrderType

admin.site.register(Asset)
admin.site.register(AssetType)
admin.site.register(Order)
admin.site.register(OrderType)
admin.site.register(Wallet)
admin.site.register(Wallet_Asset)