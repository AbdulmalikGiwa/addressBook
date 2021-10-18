from rest_framework.serializers import ModelSerializer

from address.models import Address


class AddressSerializer(ModelSerializer):

    def create(self, validated_data):
        user_id = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user_id = request.user.id
        validated_data['user_id'] = user_id
        return super(AddressSerializer, self).create(validated_data)

    class Meta:
        model = Address
        exclude = ["user", ]


class AddressReadOnlySerializer(ModelSerializer):
    """Serializer for read/list of addresses which will not include user id"""

    class Meta:
        model = Address
        exclude = ("user",)
