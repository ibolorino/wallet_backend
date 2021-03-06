from django.urls import path

from my_wallet.wallets.api.views import (
    OrderListCreateView,
    OrderRetrieveUpdateDestroyView,
    WalletListView,
    WalletRetrieveUpdateDestroyView,
    AssetTypeListCreateView,
    AssetTypeRetrieveUpdateDestroyView,
    AssetListCreateView,
    AssetRetrieveUpdateDestroyView,
    WalletChartView
)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from my_wallet.users.api.views import TokenObtainPairView, UserCreateView


urlpatterns = [
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('register', UserCreateView.as_view()),
    path('orders', OrderListCreateView.as_view()),
    path('orders/<int:pk>', OrderRetrieveUpdateDestroyView.as_view()),
    path('my_wallet', WalletListView.as_view()),
    path('my_wallet/chart', WalletChartView.as_view()),
    path('my_wallet/<int:pk>', WalletRetrieveUpdateDestroyView.as_view()),
    path('asset_type', AssetTypeListCreateView.as_view()),
    path('asset_type/<int:pk>', AssetTypeRetrieveUpdateDestroyView.as_view()),
    path('asset', AssetListCreateView.as_view()),
    path('asset/<int:pk>', AssetRetrieveUpdateDestroyView.as_view()),
]