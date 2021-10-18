from django.http import JsonResponse
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from generics.views import BaseViewSet
from .exceptions import NoDataException
from .models import Address

from .serializers import AddressSerializer, AddressReadOnlySerializer
from django_filters.rest_framework import DjangoFilterBackend


class AddressViewset(BaseViewSet):
    permission_classes = [IsAuthenticated, ]
    authentication_classes = [TokenAuthentication, ]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["country", "state", "postal_code"]

    def get_queryset(self):
        user = self.request.user

        return Address.objects.filter(user=user)

    def get_serializer_class(self):
        if self.action == "retrieve" or self.action == "list":
            return AddressReadOnlySerializer
        elif self.action is not None:
            return super().get_serializer_class()

    @action(detail=False, methods=['POST'], name='Delete multiple addresses', url_path="bulk-delete")
    def delete_bulk(self, request):
        ids = request.data.get('ids', [])
        ids = list(ids)
        if len(ids) == 0:
            raise NoDataException

        if not all(isinstance(id, int) for _id in ids):  # Checks if all ids passed are integers
            raise ValidationError({"error": "Expecting integer type only"})

        Address.objects.filter(user=request.user, id__in=input).delete()
        return JsonResponse({"message": "bulk delete successful"}, status=status.HTTP_200_OK)
