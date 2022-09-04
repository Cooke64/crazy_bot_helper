from rest_framework import serializers

from users.models import TelegramUsers


class TelegramUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = TelegramUsers
        fields = ('chat_id', 'username')