from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from hashids import Hashids

User = get_user_model()
hashids = Hashids(salt="your_secret_salt")

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'iin', 'first_name', 'last_name', 'middle_name', 'password', 'date_of_birth', 'date_joined', 'hashed_id')
        read_only_fields = ('id', 'date_joined', 'hashed_id')

    def create(self, validated_data):
        user = User.objects.create_user(
            phone_number=validated_data['phone_number'],
            iin=validated_data['iin'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            middle_name=validated_data.get('middle_name', ''),
            password=validated_data['password'],
            date_of_birth=validated_data['date_of_birth']
        )
        user.hashed_id = hashids.encode(user.id)
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        phone_number = data.get('phone_number')
        password = data.get('password')

        if phone_number and password:
            user = authenticate(phone_number=phone_number, password=password)
            if not user:
                raise serializers.ValidationError("Invalid credentials")
        else:
            raise serializers.ValidationError("Must include 'phone_number' and 'password'")
        data['user'] = user
        return data


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'iin', 'first_name', 'last_name', 'middle_name', 'date_of_birth', 'date_joined', 'hashed_id')
