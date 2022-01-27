from rest_framework import serializers
from my_wallet.apiv1.mixins import PrefetchedSerializer
from my_wallet.wallets.models import (
    Asset, 
    AssetType, 
    Order,
    OrderType,
    Wallet_Asset,
)
from my_wallet.users.api.serializers import User, UserSerializer
from my_wallet.apiv1.validators import GreaterThanZeroValidator

class AssetTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = AssetType
        fields = '__all__'


class AssetSerializer(serializers.ModelSerializer, PrefetchedSerializer):
    class Meta:
        model = Asset
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['asset_type'] = AssetTypeSerializer(instance.asset_type).data
        return data


class AssetUpdateSerializer(AssetSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False)
    ticker = serializers.CharField(required=False)
    asset_type = serializers.PrimaryKeyRelatedField(required=False, queryset=AssetType.objects.all())


class OrderTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderType
        fields = '__all__'
        

class OrderSerializer(serializers.ModelSerializer, PrefetchedSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    quantity = serializers.IntegerField(validators=[GreaterThanZeroValidator(),])

    class Meta:
        model = Order
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['asset'] = AssetSerializer(instance.asset).data
        data['user'] = UserSerializer(instance.user).data
        data['order_type'] = OrderTypeSerializer(instance.order_type).data
        return data


class OrderUpdateSerializer(serializers.ModelSerializer, PrefetchedSerializer):
    id = serializers.IntegerField(read_only=True)
    asset = serializers.StringRelatedField(read_only=True)
    order_type = serializers.StringRelatedField(read_only=True)
    order_date = serializers.DateField(required=False)
    quantity = serializers.IntegerField(required=False)
    value = serializers.FloatField(required=False)

    class Meta:
        model = Order
        fields = ('id', 'asset', 'order_type', 'order_date', 'quantity', 'value')


class WalletSerializer(serializers.ModelSerializer, PrefetchedSerializer):
    id = serializers.IntegerField(read_only=True)
    asset = AssetSerializer()

    class Meta:
        model = Wallet_Asset
        fields = ('id', 'asset', 'quantity', 'invested_amount', 'average_price')


class WalletUpdateSerializer(WalletSerializer):
    asset = serializers.StringRelatedField(read_only=True)


class WalletChartSerializer(serializers.ModelSerializer, PrefetchedSerializer):
    id = serializers.CharField(source='asset.ticker')
    label = serializers.CharField(source='asset.ticker')
    value = serializers.FloatField(source='current_value')

    class Meta:
        model = Wallet_Asset
        fields = ('id', 'label', 'value')