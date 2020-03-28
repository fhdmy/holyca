from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import generics, permissions, views, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action, permission_classes
import account.models
import account.serializers
import base64
from caserver.authentication import has_expired

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = account.serializers.UserSerializer
    filter_fields = ['username']
    ordering_fields = '__all__'

class TeammateViewSet(viewsets.ModelViewSet):
    queryset = account.models.Teammate.objects.all()
    serializer_class=account.serializers.TeammateSerializer

    @action(methods=['post'],detail=False,permission_classes=[permissions.IsAuthenticated])
    def change_pwd(self, request, *args, **kwargs):
        user = request.user
        serializer = account.serializers.ChangePwdSerializer(
            data=request.data
        )
        if serializer.is_valid():
            p0 = request.data['old_pwd']
            p0 = str(base64.decodebytes(bytes(p0, 'utf-8')), 'utf-8')
            p1 = request.data['new_pwd']
            p1 = str(base64.decodebytes(bytes(p1, 'utf-8')), 'utf-8')
            user = authenticate(
                username=user.username,
                password=p0
            )
            if not user:
                return Response('Password does not match', 400)
            user.set_password(p1)
            user.save()
            return Response('Change password OK')
        return Response('Serializer is invalid', 400)
    
    @action(methods=['post'], detail=False, permission_classes=[permissions.AllowAny])
    def login(self, request, *args, **kwargs):
        serializer = account.serializers.LoginSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            user = serializer.validated_data['user']
            if has_expired(user.auth_token):
                user.auth_token.delete()
            token, created = Token.objects.get_or_create(user=user)
            user_id = str(user.id)
            profile_id = str(user.teammate.id)
            return Response({
                'token': token.key,
                'user_id': user_id,
                'profile_id': profile_id,
            })
        else:
            return Response('Account verification failed', 400)
    
    @action(methods=['get'], detail=False, permission_classes=[permissions.IsAuthenticated])
    def get_homepage(self, request, *args, **kwargs):
        instance = request.user.teammate
        serializer = account.serializers.TeammateHomepageSerializer(
            instance=instance,
            context={'request': request}
        )
        return Response(serializer.data)

class SignUp(views.APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        serializer = account.serializers.SignUpSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            p = request.data['password']
            p = str(base64.decodebytes(bytes(p, 'utf-8')), 'utf-8')
            try:
                new_user = User.objects.create_user(
                    username=request.data['username'],
                    password=p,
                )
            except:
                return Response('Username already exisits', 400)
            token, created = Token.objects.get_or_create(user=new_user)
            account.models.Teammate.objects.create(
                user=new_user,
                nickname=request.data['username'],
            )
            user_id = str(new_user.id)
            profile_id = str(new_user.teammate.id)
            return Response({
                'token': token.key,
                'user_id': user_id,
                'profile_id': profile_id,
            }, 201)
        return Response('Serializer is invalid', 400)