class PrefetchedSerializer():
    """
        Mixin utilizado para otimizar a serialização de Nested Serializers.
    """
    @staticmethod
    def select_related_queryset(queryset, args):
        queryset = queryset.select_related(*args)
        return queryset

    @staticmethod
    def prefetch_related_queryset(queryset, args):
        queryset = queryset.prefetch_related(*args)
        return queryset