from djoser import serializers
from .models import CustomUser, Agent, Customer
import logging

logger = logging.getLogger(__name__)

class CustomUserCreateSerializer(serializers.UserCreateSerializer):
    class Meta(serializers.UserCreateSerializer.Meta):
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'address', 'phoneNumber', 'password', 'user_type']

    def create(self, validated_data):
        user_type = validated_data['user_type']

        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        # Create Agent or Customer based on user_type
        if user_type == 'agent':
            agent = Agent.objects.create(user=user)
            logger.info("Agent created for user: %s", user.username)
        elif user_type == 'customer':
            customer = Customer.objects.create(user=user)
            logger.info("Customer created for user: %s", user.username)

        return user
