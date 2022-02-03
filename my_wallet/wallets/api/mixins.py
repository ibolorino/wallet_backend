
class TotalWalletMixin():
    def get_serializer_context(self):
            context = super().get_serializer_context()
            qs = self.get_queryset()
            total = 0
            for item in qs:
                total += item.current_value
            context.update({'total': total})
            return context