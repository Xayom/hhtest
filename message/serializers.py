from rest_framework import serializers
from .models import Messagefromsky


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messagefromsky
        fields = ("id", "date", "text", "seen")
