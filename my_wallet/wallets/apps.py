from django.apps import AppConfig


class WalletsConfig(AppConfig):
    name = "my_wallet.wallets"
    verbose_name = "Wallets"

    def ready(self):
        import my_wallet.wallets.signals
