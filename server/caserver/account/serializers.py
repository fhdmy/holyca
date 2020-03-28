from rest_framework import serializers
import account.models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.utils.encoding import smart_text
from rest_framework.authtoken.serializers import AuthTokenSerializer
import base64

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class TeammateSerializer(serializers.ModelSerializer):
    class Meta:
        model = account.models.Teammate
        fields = '__all__'

class ChangePwdSerializer(serializers.Serializer):
    old_pwd = serializers.CharField()
    new_pwd = serializers.CharField()

class LoginSerializer(AuthTokenSerializer):
    def validate(self, attrs):
        try:
            username = account.models.Teammate.objects.get(
                nickname=attrs['username'],
            ).user.username
        except account.models.Teammate.DoesNotExist:
            username = get_random_string(
                length=8,
                allowed_chars="abcdefghijklmnopqrstuvwxyz0123456789",
            )
        attrs['username'] = username
        p = attrs['password']
        attrs['password'] = smart_text(base64.decodebytes(bytes(p, 'utf-8')))
        return super().validate(attrs)

class TeammateHomepageSerializer(serializers.ModelSerializer):
    class Meta:
        model = account.models.Teammate
        fields = ['nickname','score','auth','repstats_acc','repstats_pwd']

class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
