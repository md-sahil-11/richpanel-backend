from django.conf import settings
from rest_framework import serializers
from subscription.models import Device, Plan, SubscriptionHistory
from user.api.serializers import UserSerializer

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('name',)


class PlanSerializer(serializers.ModelSerializer):
    devices = DeviceSerializer(read_only=True, many=True)
    devices_str = serializers.SerializerMethodField()

    class Meta:
        model = Plan
        fields = (
            "id",
            "price_id",
            "plan_name",
            "price",
            "video_quality",
            "membership",
            "resolution",
            "devices",
            "devices_str",
            "screens"
        )
        read_only_fields = (
            "date_joined",
            "price_id",
            "membership"
        )
    
    def get_devices_str(self, instance):
        devices_name = instance.devices.all().values('name')
        result = ""
        for i in devices_name:
            result += "+ " +i['name'] + " "
        return result[1:]


class SubscriptionHistorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    plan = PlanSerializer(read_only=True)

    class Meta:
        model = SubscriptionHistory
        fields = (
            "id",
            "user",
            "plan",
            "is_cancelled"
        )
        read_only_fields = (
            "is_cancelled",
        )