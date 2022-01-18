from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Order, Wallet, OrderType, Wallet_Asset
from rest_framework.serializers import ValidationError

# TODO: corrigir bug -> ao atualizar Order, o Wallet é atualizado a partir do valor vigente

@receiver(pre_save, sender=Order)
def validate_order(sender, instance, *args, **kwargs):
    user_wallet = Wallet_Asset.objects.filter(wallet__user=instance.user, asset=instance.asset)
    if user_wallet.exists() and instance.order_type == OrderType.sell_order():
        if instance.quantity > user_wallet[0].quantity:
            raise ValidationError({'quantity': ['A quantidade final de sua carteira não pode ser menor que 0.']})


@receiver(post_save, sender=Order)
def update_wallet_on_new_order(sender, instance, update_fields, created, *args, **kwargs):
    user_wallet = Wallet.objects.filter(user=instance.user)
    if user_wallet.exists():
        if created:
            user_wallet[0].update_wallet(instance)
    else:
        instance.create_wallet()

#@receiver(post_delete, sender=Order)
# def update_wallet_on_delete(sender, instance, *args, **kwargs):
#     user_wallet = Wallet_Asset.objects.filter(wallet__user=instance.user, asset=instance.asset)
#     if user_wallet.exists():
#         user_wallet[0].delete_order(instance)

