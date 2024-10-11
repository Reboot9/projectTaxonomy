from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ["id", "email"]


class UserRegistrationSerializer(BaseUserSerializer):
    password = serializers.CharField(
        max_length=128, min_length=8, style={"input_type": "password"}, write_only=True
    )


    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ["password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class UserLoginSerializer(BaseUserSerializer):
    password = serializers.CharField(write_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ["password"]