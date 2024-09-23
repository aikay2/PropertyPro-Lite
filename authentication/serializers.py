from rest_framework import serializers
from .models import CustomUser, Agent, Customer

class CustomUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'address', 'phoneNumber', 'password', 'user_type']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user_type = validated_data.pop('user_type')

        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        # Create Agent or Customer based on user_type
        if user_type == 'agent':
            Agent.objects.create(user=user) 
        elif user_type == 'customer':
            Customer.objects.create(user=user)

        return user
