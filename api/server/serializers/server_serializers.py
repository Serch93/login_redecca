from rest_framework import serializers
from api.server.models import Server


class ServerSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    class Meta:
        model = Server
        exclude = ['is_active', 'created', 'updated']
