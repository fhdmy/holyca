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
import requests
from caserver.authentication import has_expired

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

# 定时更新signin
try:  
    # 实例化调度器
    scheduler = BackgroundScheduler()
    # 调度器使用DjangoJobStore()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    # 'cron'方式循环，周一到周五，每天9:30:10执行,id为工作ID作为标记
    # day_of_week='mon-fri', hour='9', minute='30', second='10'
    # ('scheduler',"interval", seconds=1)  #用interval方式循环，每一秒执行一次
    @register_job(scheduler, 'cron', day_of_week='0-6',hour='3',minute='0',second='0',id='task_time')
    def signin_update():
        teammates = account.models.Teammate.objects.all()
        for tm in teammates:
            tm.has_signin=False
            tm.save()

    # 监控任务
    register_events(scheduler)
    # 调度器开始
    scheduler.start()
except Exception as e:
    print(e)
    # 报错则调度器停止执行
    scheduler.shutdown()

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = account.serializers.UserSerializer
    filter_fields = ['username']
    ordering_fields = '__all__'

class TeammateViewSet(viewsets.ModelViewSet):
    queryset = account.models.Teammate.objects.all()
    serializer_class=account.serializers.TeammateSerializer

    @action(methods=['post'],detail=False,permission_classes=[permissions.IsAuthenticated])
    def alert_info(self, request, *args, **kwargs):
        user = request.user
        serializer = account.serializers.AlertInfoSerializer(
            data=request.data
        )
        if serializer.is_valid():
            # 检查密码
            p0 = request.data['password']
            p0 = str(base64.decodebytes(bytes(p0, 'utf-8')), 'utf-8')
            user = authenticate(
                username=user.username,
                password=p0
            )
            if not user:
                return Response('Password does not match', 400)
           
            #如果更改了昵称，判断昵称是否可用
            if user.teammate.nickname!=request.data['nickname']:
                try:
                    findTeammate = account.models.Teammate.objects.get(
                        nickname=request.data['nickname'],
                    )   
                    return Response('Username already exisits', 400)
                except:
                    pass
                user.teammate.nickname=request.data['nickname']
                user.teammate.save()
            
            #如果有RepStats信息，则更改
            if request.data['repstats_acc']!="" or request.data['repstats_pwd']!="" or request.data['auth']!="":
                r_acc=user.teammate.repstats_acc
                r_pwd=user.teammate.repstats_pwd
                r_auth=user.teammate.auth
                rp = request.data['repstats_pwd']
                rp = str(base64.decodebytes(bytes(rp, 'utf-8')), 'utf-8')
                #如果发生改动
                if r_acc!=request.data['repstats_acc'] or r_pwd!=rp or r_auth!=request.data['auth']:
                    repstats_login_flag=True
                    #登录账号
                    login_url="https://sc2replaystats.com/Account/signin"
                    req_data={
                        "email":request.data['repstats_acc'],
                        "password":rp
                    }
                    req_header={
                        "Authorization":request.data['auth']
                    }
                    res=requests.post(login_url,data=req_data,headers=req_header)
                    if res.status_code==200:
                        if "Failed to login, please try your email and password again." in res.text:
                            repstats_login_flag=False
                    else:
                        repstats_login_flag=False

                    if not repstats_login_flag:
                        return Response('RepStats verification is invalid', 400)
                    user.teammate.repstats_acc=request.data['repstats_acc']
                    user.teammate.repstats_pwd=rp
                    user.teammate.auth=request.data['auth']
                    user.teammate.save()
            
            #更改密码
            if request.data['new_password']!="":
                np=request.data['new_password']
                np=str(base64.decodebytes(bytes(np, 'utf-8')), 'utf-8')
                user.set_password(np)
                user.save()
            return Response('Alter Info OK')
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
            return Response('Serializer is invalid', 400)
    
    @action(methods=['get'], detail=False, permission_classes=[permissions.IsAuthenticated])
    def get_homepage(self, request, *args, **kwargs):
        instance = request.user.teammate
        serializer = account.serializers.TeammateHomepageSerializer(
            instance=instance,
            context={'request': request}
        )
        return Response(serializer.data)
    
    @action(methods=['post'],detail=False,permission_classes=[permissions.IsAuthenticated])
    def signin(self, request, *args, **kwargs):
        user = request.user
        has_signin=user.teammate.has_signin
        if not has_signin:
            user.teammate.has_signin=True
            score=user.teammate.score
            user.teammate.score=score+20
            user.teammate.save()
            return Response("Signin OK")
        return Response("User has signined today",400)

class SignUp(views.APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        serializer = account.serializers.SignUpSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            # 站内密码
            p = request.data['password']
            p = str(base64.decodebytes(bytes(p, 'utf-8')), 'utf-8')
            
            # repstats密码
            rp = request.data['repstats_pwd']
            rp = str(base64.decodebytes(bytes(rp, 'utf-8')), 'utf-8')

            #test repstats
            repstats_login_flag=True
            if request.data['repstats_acc']!="":
                #登录账号
                login_url="https://sc2replaystats.com/Account/signin"
                req_data={
                    "email":request.data['repstats_acc'],
                    "password":rp
                }
                req_header={
                    "Authorization":request.data['auth']
                }
                res=requests.post(login_url,data=req_data,headers=req_header)
                if res.status_code==200:
                    if "Failed to login, please try your email and password again." in res.text:
                        repstats_login_flag=False
                else:
                    repstats_login_flag=False

            if not repstats_login_flag:
                return Response('RepStats verification is invalid', 400)
                
            try:
                new_user = User.objects.create_user(
                    username=request.data['nickname'],
                    password=p,
                )
            except:
                return Response('Username already exisits', 400)

            try:
                findTeammate = account.models.Teammate.objects.get(
                    nickname=request.data['nickname'],
                )   
                return Response('Username already exisits', 400)
            except:
                pass

            token, created = Token.objects.get_or_create(user=new_user)
            account.models.Teammate.objects.create(
                user=new_user,
                nickname=request.data['nickname'],
                auth=request.data['auth'],
                repstats_acc=request.data['repstats_acc'],
                repstats_pwd=rp
            )
            user_id = str(new_user.id)
            profile_id = str(new_user.teammate.id)
            return Response({
                'token': token.key,
                'user_id': user_id,
                'profile_id': profile_id,
            }, 201)
        return Response('Serializer is invalid', 400)