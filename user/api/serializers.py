from django.conf import settings
from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "name",
            "date_joined",
            "subscription",
            "customer",
        )
        read_only_fields = (
            "date_joined",
            "subscription",
            "customer",
        )