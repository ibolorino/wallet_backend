from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from my_wallet.apiv1.permissions import IsAadminOrReadOnly
from rest_framework.serializers import ValidationError
from .serializers import (
    AssetSerializer,
    AssetUpdateSerializer,
    AssetTypeSerializer,
    OrderSerializer, 
    OrderUpdateSerializer, 
    WalletSerializer,
    WalletUpdateSerializer,
)
from my_wallet.wallets.models import Asset, AssetType, Order, Wallet_Asset


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        if queryset:
            queryset = self.get_serializer_class().select_related_queryset(queryset, ['asset', 'user', 'order_type', 'asset__asset_type'])
        return queryset


class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_serializer_class(self):
        """
            O método PUT utiliza um serializer específico devido ao requerimento de alguns campos.
        """
        if self.request.method == 'PUT':
            return OrderUpdateSerializer
        return OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)
        if queryset:
            queryset = self.get_serializer_class().select_related_queryset(queryset, ['asset', 'user', 'order_type', 'asset__asset_type'])
        return queryset


class WalletListView(generics.ListAPIView):
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Wallet_Asset.objects.filter(wallet__user=self.request.user, quantity__gt=0)
        if queryset:
            queryset = self.get_serializer_class().select_related_queryset(queryset, ['asset', 'asset__asset_type'])
        return queryset

class WalletRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WalletUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        queryset = Wallet_Asset.objects.filter(wallet__user=self.request.user, quantity__gt=0)
        if queryset:
            queryset = self.get_serializer_class().select_related_queryset(queryset, ['asset', 'asset__asset_type'])
        return queryset


class AssetTypeListCreateView(generics.ListCreateAPIView):
    serializer_class = AssetTypeSerializer
    permission_classes = [IsAadminOrReadOnly]
    queryset = AssetType.objects.all()


class AssetTypeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AssetTypeSerializer
    permission_classes = [IsAadminOrReadOnly]
    queryset = AssetType.objects.all()
    lookup_field = 'pk'


class AssetListCreateView(generics.ListCreateAPIView):
    serializer_class = AssetSerializer
    permission_classes = [IsAadminOrReadOnly]
    queryset = Asset.objects.all()


class AssetRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAadminOrReadOnly]
    queryset = Asset.objects.all()
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return AssetUpdateSerializer
        return AssetSerializer