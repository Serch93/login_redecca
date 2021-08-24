from rest_framework import serializers

from api.investigator.models import Investigator, Codes


class LoginUserKeycloakSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, min_length=10, max_length=100)
    password = serializers.CharField(
        required=True, min_length=8, max_length=60, write_only=True)
    token_type = serializers.CharField(read_only=True)
    access_token = serializers.CharField(read_only=True)
    refresh_token = serializers.CharField(read_only=True)


class LogoutKeycloakSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)


class GetInfoSerializer(serializers.Serializer):
    sub = serializers.CharField()
    cvu = serializers.CharField()
    email_verified = serializers.BooleanField()
    updated_at = serializers.DateTimeField()
    name = serializers.CharField()
    preferred_username = serializers.CharField()
    internal_user = serializers.BooleanField()
    given_name = serializers.CharField()
    family_name = serializers.CharField()
    email = serializers.EmailField()
    curp = serializers.CharField()


class SendCodeResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    curp = serializers.CharField(required=True, min_length=15, max_length=50)
    user = None

    def validate(self, attrs):
        email = attrs.get("email")
        curp = attrs.get("curp")

        user = Investigator.objects.filter(
            email__icontains=email, curp__icontains=curp)

        if not user.exists():
            raise serializers.ValidationError(
                {"error_description": "Credenciales incorrectas, verifique su información"})

        self.user = user[0]
        return super().validate(attrs)

    def create(self, validated_data):
        instance, created = Codes.objects.get_or_create(investigator=self.user)
        instance.code=validated_data
        instance.save()
        self.user.is_active = False
        self.user.save()
