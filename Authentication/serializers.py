# Core
from rest_framework import serializers

# Dev
from Authentication.models import User
from encryption.symmetric.key_generator import generateAESKey


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create(
            name=validated_data['name'],
            role=validated_data['role'],
            national_id=validated_data['national_id'],
            university=validated_data['university']
        )
        user.symmetric_key = generateAESKey(validated_data['national_id'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('name', 'password', 'university', 'role', 'national_id')
