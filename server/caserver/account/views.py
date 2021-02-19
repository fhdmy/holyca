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
import match.models
from caserver.authentication import has_expired
from datetime import timedelta
from datetime import datetime
from match.apis import API

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
    # @register_job(scheduler, 'interval', seconds=1,id='test')
    @register_job(scheduler, 'cron', day_of_week='0-6',hour='3',minute='0',second='0',id='update_signin')
    def signin_update():
        teammates = account.models.Teammate.objects.all()
        for tm in teammates:
            tm.has_signin=False
            tm.save()
        print(str(datetime.now())+": signin_updated")
        # print(test)

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

class RepStatsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = account.models.RepStats.objects.all()
    serializer_class = account.serializers.RepStatsSerializer
    filter_fields = ['repstats_id']
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
            if str(user.teammate.nickname)!=request.data['nickname']:
                try:
                    findTeammate = account.models.Teammate.objects.get(
                        nickname=request.data['nickname'],
                    )   
                    return Response('Username already exisits', 400)
                except Exception as e:
                    print(e)
                user.teammate.nickname=request.data['nickname']
                user.teammate.save()
            
            #如果有RepStats信息，则更改
            if request.data['repstats_acc']!="" or request.data['repstats_pwd']!="" or request.data['auth']!="":
                r_acc=user.teammate.repstats.repstats_acc
                r_pwd=user.teammate.repstats.repstats_pwd
                r_auth=user.teammate.repstats.auth
                rp = request.data['repstats_pwd']
                rp = str(base64.decodebytes(bytes(rp, 'utf-8')), 'utf-8')
                #如果发生改动
                if str(r_acc)!=request.data['repstats_acc'] or str(r_pwd)!=rp or str(r_auth)!=request.data['auth']:
                    # 如果其他账号有此repstats号
                    rs=account.models.RepStats.objects.all()
                    for r in rs:
                        if str(r.repstats_acc)==request.data['repstats_acc'] and str(r.teammate)!=request.data['nickname']:
                            return Response('RepStats already used', 400)

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
                    user.teammate.repstats.repstats_acc=request.data['repstats_acc']
                    user.teammate.repstats.repstats_pwd=rp
                    user.teammate.repstats.auth=request.data['auth']
                    user.teammate.repstats.save()
            
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
    
    @action(methods=['get'], detail=False, permission_classes=[permissions.IsAuthenticated])
    def get_score(self, request, *args, **kwargs):
        teammate = request.user.teammate
        score=teammate.score
        return Response(score)
    
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
    
    @action(methods=['get'],detail=False,permission_classes=[permissions.IsAuthenticated])
    def mmr_statistics(self, request, *args, **kwargs):
        user = request.user
        day_long=7
        today = datetime.today()
        info=[]
        mmr_record=[]
        for i in range(11,-1,-1):
            players=[]
            mmr_record.append({})
            info.append([])
            for bn in user.teammate.repstats.battlenet_acc.all():
                if bn in players:
                    continue
                mmr_T={"sum":0,"num":0}
                mmr_P={"sum":0,"num":0}
                mmr_Z={"sum":0,"num":0}
                mmrs=match.models.MMR.objects.filter(
                    date__range=(today-timedelta(days=day_long*(i+1)),today-timedelta(days=day_long*i)),
                    battlenet_acc=bn
                ).order_by("-date")
                mmr_sum=0
                mmr_num=0
                for mmr in mmrs:
                    if mmr.mmr!=0:
                        if mmr.race=="P":
                            mmr_P["sum"]+=mmr.mmr
                            mmr_P["num"]+=1
                        elif mmr.race=="Z":
                            mmr_Z["sum"]+=mmr.mmr
                            mmr_Z["num"]+=1
                        else:
                            mmr_T["sum"]+=mmr.mmr
                            mmr_T["num"]+=1
                mmr_avg=0
                # 向前寻找mmr非0的点并赋值
                if mmr_T["sum"]==0 and mmr_P["sum"]==0 and mmr_Z["sum"]==0:
                    k=0
                    while k<12:
                        # 先从mmr_record查找
                        if i<11:
                            if mmr_record[11-i-1][bn.battlenet_name]!=0:
                                # 替换
                                mmr_avg=(int)(mmr_record[11-i-1][bn.battlenet_name])
                                break
                        former_mmrs=match.models.MMR.objects.filter(
                            date__range=(today-timedelta(days=day_long*(i+1+k)),today-timedelta(days=day_long*(i+k))),
                            battlenet_acc=bn
                        ).order_by("-date")
                        tempmmr_T={"sum":0,"num":0}
                        tempmmr_P={"sum":0,"num":0}
                        tempmmr_Z={"sum":0,"num":0}
                        for former_mmr in former_mmrs:
                            if former_mmr.mmr!=0:
                                if former_mmr.race=="P":
                                    tempmmr_P["sum"]+=former_mmr.mmr
                                    tempmmr_P["num"]+=1
                                elif former_mmr.race=="Z":
                                    tempmmr_Z["sum"]+=former_mmr.mmr
                                    tempmmr_Z["num"]+=1
                                else:
                                    tempmmr_T["sum"]+=former_mmr.mmr
                                    tempmmr_T["num"]+=1
                        #选择最大的mmr
                        if tempmmr_Z["num"]==0:
                            tempmmr_avg_Z=0
                        else:
                            tempmmr_avg_Z=(int)(tempmmr_Z["sum"]/tempmmr_Z["num"])
                        if tempmmr_P["num"]==0:
                            tempmmr_avg_P=0
                        else:
                            tempmmr_avg_P=(int)(tempmmr_P["sum"]/tempmmr_P["num"])
                        if tempmmr_T["num"]==0:
                            tempmmr_avg_T=0
                        else:
                            tempmmr_avg_T=(int)(tempmmr_T["sum"]/tempmmr_T["num"])
                        tempmmr_avg=max(tempmmr_avg_Z,tempmmr_avg_P,tempmmr_avg_T)
                        # 替换
                        if tempmmr_avg!=0:
                            mmr_avg=tempmmr_avg
                            break
                        k+=1

                else:
                    #选择最大的mmr
                    if mmr_Z["num"]==0:
                        mmr_avg_Z=0
                    else:
                        mmr_avg_Z=(int)(mmr_Z["sum"]/mmr_Z["num"])
                    if mmr_P["num"]==0:
                        mmr_avg_P=0
                    else:
                        mmr_avg_P=(int)(mmr_P["sum"]/mmr_P["num"])
                    if mmr_T["num"]==0:
                        mmr_avg_T=0
                    else:
                        mmr_avg_T=(int)(mmr_T["sum"]/mmr_T["num"])
                    mmr_avg=max(mmr_avg_Z,mmr_avg_P,mmr_avg_T)

                info[11-i].append({
                    "name":bn.battlenet_name,
                    "mmr":mmr_avg,
                    "date":today-timedelta(days=day_long*i+day_long/2),
                })
                mmr_record[11-i][bn.battlenet_name]=mmr_avg
                players.append(bn)
        
        return Response(info)

    @action(methods=['get'],detail=False,permission_classes=[permissions.IsAuthenticated])
    def racesum_statistics(self, request, *args, **kwargs):
        user = request.user
        #获得最近一个月每个账号rep对手的种族
        today = datetime.today()
        reps=match.models.Replay.objects.filter(
            date__range=(today-timedelta(days=30),today),
            repstats_acc=user.teammate.repstats
        ).order_by("-date")
        p_sum=0
        z_sum=0
        t_sum=0
        for r in reps:
            player1,player2=r.player1,r.player2
            player1_race,player2_race=r.vs_race.split("v")[0],r.vs_race.split("v")[1]
            if player1 in user.teammate.repstats.battlenet_acc.all():
                if player2_race=="T":
                    t_sum+=1
                elif player2_race=="P":
                    p_sum+=1
                elif player2_race=="Z":
                    z_sum+=1
            elif player2 in user.teammate.repstats.battlenet_acc.all():
                if player1_race=="T":
                    t_sum+=1
                elif player1_race=="P":
                    p_sum+=1
                elif player1_race=="Z":
                    z_sum+=1

        rtn=[
            {
                "race":"P",
                "sum":p_sum
            },
            {
                "race":"Z",
                "sum":z_sum
            },
            {
                "race":"T",
                "sum":t_sum
            }
        ]
        return Response(rtn)
    
    @action(methods=['get'],detail=False,permission_classes=[permissions.IsAuthenticated])
    def racewinrate_statistics(self, request, *args, **kwargs):
        user = request.user
        day_long=7
        today = datetime.today()
        rtn=[]
        for i in range(11,-1,-1):
            reps=match.models.Replay.objects.filter(
                date__range=(today-timedelta(days=day_long*(i+1)),today-timedelta(days=day_long*i)),
                repstats_acc=user.teammate.repstats
            ).order_by("-date")
            
            tvp_sum=0
            pvz_sum=0
            zvt_sum=0
            tvp_win=0
            pvz_win=0
            zvt_win=0
            for r in reps:
                if r.vs_race=="TvP" or r.vs_race=="PvT":
                    tvp_sum+=1
                    if r.winner==r.player1.battlenet_name and r.vs_race=="TvP":
                        tvp_win+=1
                    elif r.winner==r.player2.battlenet_name and r.vs_race=="PvT":
                        tvp_win+=1
                elif r.vs_race=="PvZ" or r.vs_race=="ZvP":
                    pvz_sum+=1
                    if r.winner==r.player1.battlenet_name and r.vs_race=="PvZ":
                        pvz_win+=1
                    elif r.winner==r.player2.battlenet_name and r.vs_race=="ZvP":
                        pvz_win+=1
                elif r.vs_race=="ZvT" or r.vs_race=="TvZ":
                    zvt_sum+=1
                    if r.winner==r.player1.battlenet_name and r.vs_race=="ZvT":
                        zvt_win+=1
                    elif r.winner==r.player2.battlenet_name and r.vs_race=="TvZ":
                        zvt_win+=1
            
            if tvp_sum==0:
                tvp_winrate=50
            else:
                tvp_winrate=round(tvp_win*100/tvp_sum,1)
            if pvz_sum==0:
                pvz_winrate=50
            else:
                pvz_winrate=round(pvz_win*100/pvz_sum,1)
            if zvt_sum==0:
                zvt_winrate=50
            else:
                zvt_winrate=round(zvt_win*100/zvt_sum,1)

            rtn.append({
                "date":today-timedelta(days=day_long*i+day_long/2),
                "TVP":tvp_winrate,
                "PVZ":pvz_winrate,
                "ZVT":zvt_winrate
            })
        return Response(rtn)

    @action(methods=['get'],detail=False,permission_classes=[permissions.IsAuthenticated])
    def active_statistics(self, request, *args, **kwargs):
        user = request.user
        #filter in 7days
        today = datetime.today()
        reps=match.models.Replay.objects.filter(       
            date__range=(today-timedelta(days=7),today),
            repstats_acc=user.teammate.repstats
        ).order_by("-date")
        return Response(len(reps))
    
    @action(methods=['get'],detail=False,permission_classes=[permissions.IsAuthenticated])
    def get_map_winrate(self, request, *args, **kwargs):
        user = request.user
        repstats=user.teammate.repstats
        battlenets_accs=repstats.battlenet_acc.all()
        map_winrates=[]
        for bn in battlenets_accs:
            if bn.map_winrate=="":
                continue
            mw=eval(bn.map_winrate)
            map_winrates.append({
                'account':bn.battlenet_name,
                'winrate':mw
            })
        return Response(map_winrates)
    
    @action(methods=['get'],detail=False,permission_classes=[permissions.IsAuthenticated])
    def get_basic_statistics(self, request, *args, **kwargs):
        user = request.user
        repstats=user.teammate.repstats
        battlenets_accs=repstats.battlenet_acc.all()
        bs=[]
        for bn in battlenets_accs:
            if bn.basic_accomplishment=="":
                continue
            mw=eval(bn.basic_accomplishment)
            bs.append({
                'account':bn.battlenet_name,
                'basic':mw
            })
        return Response(bs)

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
                # 如果其他账号有此repstats号
                rs=account.models.RepStats.objects.all()
                for r in rs:
                    if str(r.repstats_acc)==request.data['repstats_acc'] and str(r.teammate)!=request.data['nickname']:
                        return Response('RepStats already used', 400)

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
            new_repstats=account.models.RepStats.objects.create(
                auth=request.data['auth'],
                repstats_acc=request.data['repstats_acc'],
                repstats_pwd=rp
            )
            account.models.Teammate.objects.create(
                user=new_user,
                nickname=request.data['nickname'],
                repstats=new_repstats,
                score=100
            )
            user_id = str(new_user.id)
            profile_id = str(new_user.teammate.id)
            return Response({
                'token': token.key,
                'user_id': user_id,
                'profile_id': profile_id,
            }, 201)
        return Response('Serializer is invalid', 400)