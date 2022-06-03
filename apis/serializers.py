from rest_framework import serializers
from apis.models import MyHome


class MyHomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyHome
        fields = "__all__"
