from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from rest_framework import serializers


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'url',
            # 'email',
        ]


    def get_url(self, obj):
        return reverse_lazy("profiles:detail", kwargs={"username": obj.username })

