from django.shortcuts import render
from collections import defaultdict
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import generics, permissions, views, viewsets
from rest_framework.response import Response
from datetime import datetime
from datetime import timedelta
import requests
import match.models
import account.models
import match.serializers
from match.apis import API

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

def interval_mapping(Omax,Omin,Odata):
    Nmax=10
    Nmin=0
    N=(Nmax-Nmin)/(Omax-Omin)*(int(Odata)-Omin)+Nmin
    return round(N,1)

# 定时更新match数据
try:  
    # 实例化调度器
    scheduler = BackgroundScheduler()
    # 调度器使用DjangoJobStore()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    # 'cron'方式循环，周一到周五，每天9:30:10执行,id为工作ID作为标记
    # day_of_week='mon-fri', hour='9', minute='30', second='10'
    # ('scheduler',"interval", seconds=1)  #用interval方式循环，每一秒执行一次
    # @register_job(scheduler, 'interval', minutes=30,id='get_matchs')
    @register_job(scheduler, 'interval', minutes=30,id='get_matchs')
    def match_update():
        print("match_update...")
        teammates = account.models.Teammate.objects.all()
        for tm in teammates:
            try:
                # print("***********")
                repstats=tm.repstats
                if repstats=="":
                    continue
                api=API(email=repstats.repstats_acc,password=repstats.repstats_pwd,auth=repstats.auth)
                # print("login...")
                repstats_id,battlenet_info=api.login()
                # 登录失败
                if repstats_id==-1:
                    continue
                repstats.repstats_id=repstats_id
                for name,nid in battlenet_info.items():
                    #如果没有BattlenetAccount则创建
                    bn_acc,created=match.models.BattlenetAccount.objects.get_or_create(
                        battlenet_name=name,
                        battlenet_id=nid,
                    )
                    repstats.battlenet_acc.add(bn_acc)
                for bn in repstats.battlenet_acc.all():
                    if str(bn.battlenet_id) not in battlenet_info.values():
                        bn.repstats_acc.remove(repstats)

                # print("get_rep...")
                repstats.save()
                reps=api.get_rep()
                for r in reps:
                    try:
                        #如果没有BattlenetAccount则创建
                        player_1,created=match.models.BattlenetAccount.objects.get_or_create(
                            battlenet_name=r["player1"],
                            battlenet_id=r["player1_id"]
                        )
                        # print("created player1: "+str(player_1.battlenet_name)+"-"+str(player_1.battlenet_id))
                        player_2,created=match.models.BattlenetAccount.objects.get_or_create(
                            battlenet_name=r["player2"],
                            battlenet_id=r["player2_id"]
                        )
                        # print("created player2: "+str(player_2.battlenet_name)+"-"+str(player_2.battlenet_id))
                        # 新增replay
                        replay,created=match.models.Replay.objects.get_or_create(
                            rep_id=r["rep_id"],
                            player1_mmr=r["player1_mmr"],
                            player2_mmr=r["player2_mmr"],
                            winner=r["winner"],
                            date=r["date"],
                            vs_race=r["vs_race"],
                            game_length=r["game_length"],
                            game_map=r["rep_map"],
                            player1=player_1,
                            player2=player_2
                        )
                        # print("new replay: "+str(r["rep_id"])+" "+str(r["rep_map"])+" "+str(r["game_length"])+" "+str(r["vs_race"])+" "+str(r["winner"]))
                        # MMR
                        match.models.MMR.objects.get_or_create(
                            replay=replay,
                            battlenet_acc=player_1,
                            mmr=r["player1_mmr"],
                            date=r["date"],
                            race=r["vs_race"].split("v")[0]
                        )
                        # print("new MMR: "+str(player_1.battlenet_name)+" "+str(r["player1_mmr"])+" "+str(r["date"]))
                        match.models.MMR.objects.get_or_create(
                            replay=replay,
                            battlenet_acc=player_2,
                            mmr=r["player2_mmr"],
                            date=r["date"],
                            race=r["vs_race"].split("v")[1]
                        )
                        # print("new MMR: "+str(player_2.battlenet_name)+" "+str(r["player2_mmr"])+" "+str(r["date"]))
                        replay.repstats_acc.add(repstats)
                        repstats.save()
                    except:
                        pass
            except:
                pass

    @register_job(scheduler, 'interval', minutes=60,id='replay_update')
    def replay_update():
        replays=match.models.Replay.objects.all()
        print(f"replay_update...(replays: {len(replays)})")
        for rep in replays:
            try:
                if str(rep.kills)!='':
                    continue
                repstats=rep.repstats_acc.all()[0]
                api=API(email=repstats.repstats_acc,password=repstats.repstats_pwd,auth=repstats.auth)
                repstats_id,battlenet_info=api.login()
                # 登录失败
                if repstats_id==-1:
                    continue
            
                # 更新kills
                rep.kills=str(api.get_repinfo(rep.rep_id))
                rep.save()
            except:
                pass

    #设置地图胜率和基本素养
    @register_job(scheduler, 'interval', minutes=60,id='basic_update')
    def basic_update():
        teammates = account.models.Teammate.objects.all()
        print(f"basic_update...(teammates: {len(teammates)})")
        for tm in teammates:
            try:
                repstats=tm.repstats
                if repstats=="":
                    continue
                api=API(email=repstats.repstats_acc,password=repstats.repstats_pwd,auth=repstats.auth)
                repstats_id,battlenet_info=api.login()
                # 登录失败
                if repstats_id==-1:
                    continue
                for bn in repstats.battlenet_acc.all():
                    try:
                        # 地图胜率
                        map_wr=api.get_map_winrate(bn.battlenet_id)
                        bn.map_winrate=str(map_wr)
                        #基本素养
                        attack,operation,game_length,variance=api.get_style(bn.battlenet_id)
                        today = datetime.today()
                        reps=match.models.Replay.objects.filter(
                            date__range=(today-timedelta(days=90),today),
                            repstats_acc=repstats
                        )
                        kills=0
                        kill_sum=1
                        for r in reps:
                            if not (r.player1==bn or r.player2==bn):
                                continue
                            if r.kills=="":
                                continue
                            ks=eval(r.kills)
                            kills+=ks[" "+bn.battlenet_name]
                            kill_sum+=1
                        avg_kill=round(kills/kill_sum,1)

                        #区间映射
                        attack=interval_mapping(70,25,attack)
                        if attack<0:
                            attack=0
                        if attack>10:
                            attack=10
                        operation=interval_mapping(1.2,0,operation)
                        if operation<0:
                            operation=0
                        if operation>10:
                            operation=10
                        game_length=interval_mapping(26,10,game_length)
                        if game_length<0:
                            game_length=0
                        if game_length>10:
                            game_length=10
                        variance=interval_mapping(2,0,variance)
                        if variance<0:
                            variance=0
                        if variance>10:
                            variance=10
                        avg_kill=interval_mapping(28,0,avg_kill)
                        if avg_kill<0:
                            avg_kill=0
                        if avg_kill>10:
                            avg_kill=10

                        basic_accomplishment={
                            'attack':attack,
                            'operation':operation,
                            'game_length':game_length,
                            'variance':variance,
                            'kill':avg_kill
                        }
                        # print("basic_accomplishment:",basic_accomplishment)
                        bn.basic_accomplishment=str(basic_accomplishment)
                        bn.save()

                    except Exception as e:
                        print(e)
            except Exception as e:
                print(e)
    
    # @register_job(scheduler, 'interval', minutes=1,id='reset_database')
    # def reset_database():
    #     reps=match.models.Replay.objects.all()
    #     for rep in reps:
    #         rep.delete()
    #     mmrs=match.models.MMR.objects.all()
    #     for mmr in mmrs:
    #         mmr.delete()

    # 监控任务
    register_events(scheduler)
    # 调度器开始
    scheduler.start()
except Exception as e:
    print(e)
    # 报错则调度器停止执行
    scheduler.shutdown()

class MMRViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = match.models.MMR.objects.all()
    serializer_class = match.serializers.MMRSerializer
    filter_fields = ['battlenet_acc']
    ordering_fields = '__all__'

class ReplayViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = match.models.Replay.objects.all()
    serializer_class = match.serializers.ReplaySerializer
    filter_fields = ['date']
    ordering_fields = '__all__'

class BattlenetAccountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = match.models.BattlenetAccount.objects.all()
    serializer_class = match.serializers.BattlenetAccountSerializer
    filter_fields = ['battlenet_name']
    ordering_fields = '__all__'

class ActiveStatistics(views.APIView):
    authentication_classes=[]
    permission_classes = [permissions.AllowAny, ]

    def get(self, request, *args, **kwargs):
        teammates = account.models.Teammate.objects.all()
        #filter in 7days
        today = datetime.today()
        reps=match.models.Replay.objects.filter(       
            date__range=(today-timedelta(days=7),today)
        ).order_by("-date")
        rtn=[]
        for tm in teammates:
            s=0
            repstats=tm.repstats
            for rep in reps:
                if repstats in rep.repstats_acc.all():
                    s+=1
            rtn.append({
                "sum":s,
                "account":tm.nickname,
            })
        return Response(rtn)

class MMRStatistics(views.APIView):
    authentication_classes=[]
    permission_classes = [permissions.AllowAny, ]

    def get(self, request, *args, **kwargs):
        day_long=4
        today = datetime.today()
        info=[]
        mmr_record=[]
        for i in range(11,-1,-1):
            repstats=account.models.RepStats.objects.all() 
            players=[]
            mmr_record.append({})
            info.append([])
            for rp in repstats:
                for bn in rp.battlenet_acc.all():
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

class RaceSumStatistics(views.APIView):
    authentication_classes=[]
    permission_classes = [permissions.AllowAny, ]

    def get(self, request, *args, **kwargs):
        #获得最近一个月每个账号rep对手的种族
        today = datetime.today()
        reps=match.models.Replay.objects.filter(
            date__range=(today-timedelta(days=30),today)
        ).order_by("-date")
        p_sum=0
        z_sum=0
        t_sum=0
        for r in reps:
            repstats=r.repstats_acc.all()
            for rs in repstats:
                player1,player2=r.player1,r.player2
                player1_race,player2_race=r.vs_race.split("v")[0],r.vs_race.split("v")[1]
                if player1 in rs.battlenet_acc.all():
                    if player2_race=="T":
                        t_sum+=1
                    elif player2_race=="P":
                        p_sum+=1
                    elif player2_race=="Z":
                        z_sum+=1
                elif player2 in rs.battlenet_acc.all():
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

class RaceWinrateStatistics(views.APIView):
    authentication_classes=[]
    permission_classes = [permissions.AllowAny, ]

    def get(self, request, *args, **kwargs):
        day_long=4
        today = datetime.today()
        rtn=[]
        for i in range(11,-1,-1):
            reps=match.models.Replay.objects.filter(
                date__range=(today-timedelta(days=day_long*(i+1)),today-timedelta(days=day_long*i))
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

class ReplayStatistics(views.APIView):
    authentication_classes=[]
    permission_classes = [permissions.AllowAny, ]

    def get(self, request, *args, **kwargs):
        params = request.query_params
        num=int(params['replays'])
        #最近的num个rep
        today = datetime.today()
        if num==-1:
            reps=match.models.Replay.objects.all().order_by("-date")
        else:
            reps=match.models.Replay.objects.all().order_by("-date")[:num]
        serializer = match.serializers.RecentReplaySerializer(
            instance=reps,
            context={'request': request},
            many=True
        )
        return Response(serializer.data)