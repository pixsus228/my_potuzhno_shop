from django.contrib.auth.models import User
from rest_framework import serializers

from apps.accounts.models import Profile


class UserSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source='profile.phone', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'email', 'phone']

class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['phone', 'password', 'first_name']

    def create(self, validated_data):
        phone = validated_data.pop('phone')
        user = User.objects.create_user(username=phone, **validated_data)
        Profile.objects.create(user=user, phone=phone)
        return user

