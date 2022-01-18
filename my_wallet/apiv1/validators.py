from rest_framework.serializers import ValidationError


class GreaterThanZeroValidator():

    def __call__(self, value):
        if value <= 0:
            message = 'Valor deve ser maior que 0'
            raise ValidationError(message)


# class Teste():
#     requires_context = True

#     def __call__(self, value, serializer_field):
#         print('serializer validtor')
#         serializer = serializer_field.parent
#         print(serializer.initial_data)
#         if value == -10:
#             message = 'Teste erro'
#             raise ValidationError(message)