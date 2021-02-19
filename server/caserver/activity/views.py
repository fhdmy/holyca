from django.shortcuts import render
from collections import defaultdict
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import generics, permissions, views, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from datetime import datetime
from datetime import timedelta
import activity.models
import activity.serializers
from activity.tl import TL
from activity.gs import GS

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job

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
    @register_job(scheduler, 'cron', day_of_week='0-6',hour='0',minute='0',second='0',id='get_promatches')
    # @register_job(scheduler, 'interval', minutes=2,id='get_promatches')
    def get_promatches():
        print("get_promatches...")
        #clear
        # m=activity.models.Match.objects.all()
        # for i in m:
        #     i.delete()
        # b=activity.models.Bet.objects.all()
        # for i in b:
        #     i.delete()
        tl=TL()
        matches=tl.get_upcoming_rep()
        for match in matches:
            try:
                activity.models.Match.objects.get_or_create(
                    tournament=match["match_name"],
                    match_time=match["match_time"]
                )
            except Exception as e:
                print(e)
    
    @register_job(scheduler, 'interval', minutes=15,id='get_bets') #15min
    def get_bets():
        print("get_bets...")

        gs=GS()
        matches=gs.get_matches()
        for match in matches:
            if match["time"]!="Live":
                activity.models.Bet.objects.get_or_create(
                    player_1=match["player_1"],
                    player_2=match["player_2"],
                    tournament=match["tournament"],
                    match_url=match["match_url"],
                    match_time=match["time"]
                )
            else:
                activity.models.Bet.objects.get_or_create(
                    player_1=match["player_1"],
                    player_2=match["player_2"],
                    tournament=match["tournament"],
                    match_url=match["match_url"],
                )
        
        # 如果到达比赛时间，则停止下注
        now=datetime.now()
        bets=activity.models.Bet.objects.filter(
            match_time__lt=now,
            stop_bet=False,
            finished=False
        ).order_by("-match_time")
        for bet in bets:
            bet.stop_bet=True
            bet.save()
        
        #如果比赛结束，则结算
        may_finish_bets=activity.models.Bet.objects.filter(
            match_time__lt=now-timedelta(hours=1),
            stop_bet=True,
            finished=False
        ).order_by("-match_time")
        print("get_results...")
        for may_finish_bet in may_finish_bets:
            winner,score=gs.get_results(may_finish_bet.match_url)
            if winner=="" or score=="":
                # 如果发生错误，则取消此单
                if may_finish_bet.match_time<now-timedelta(days=7):
                    #还原下注
                    re_invests=activity.models.Invest.objects.filter(
                        settled=False,
                        bet=may_finish_bet
                    )
                    for re_invest in re_invests:
                        re_invest.teammate.score+=re_invest.score
                        re_invest.teammate.save()
                        re_invest.settled=True
                        re_invest.gain=re_invest.score
                        re_invest.save()
                    
                    #设置为finished
                    may_finish_bet.finished=True
                    may_finish_bet.winner=winner
                    may_finish_bet.score=score
                    may_finish_bet.save()
            else:
                #下注结算
                settle_invests=activity.models.Invest.objects.filter(
                    settled=False,
                    bet=may_finish_bet
                )
                
                score_1=0
                score_2=0
                for iv in settle_invests:
                    if str(iv.target)==str(may_finish_bet.player_1):
                        score_1+=int(iv.score)
                    elif str(iv.target)==str(may_finish_bet.player_2):
                        score_2+=int(iv.score)
                bet_1=0
                bet_2=0
                if score_1==0 and score_2==0:
                    bet_1=0
                    bet_2=0
                elif score_1==0 and score_2!=0:
                    bet_1=0
                    bet_2=1
                elif score_2==0 and score_1!=0:
                    bet_2=0
                    bet_1=1
                else:
                    bet_1=round((score_1+score_2)/score_1,1)
                    bet_2=round((score_1+score_2)/score_2,1)

                for settle_invest in settle_invests:
                    if str(settle_invest.target)==str(winner):
                        if str(settle_invest.target)==str(may_finish_bet.player_1):
                            settle_invest.teammate.score+=int(settle_invest.score*bet_1)
                            settle_invest.gain=int(settle_invest.score*bet_1)
                        elif str(settle_invest.target)==str(may_finish_bet.player_2):
                            settle_invest.teammate.score+=int(settle_invest.score*bet_2)
                            settle_invest.gain=int(settle_invest.score*bet_2)
                    
                    settle_invest.settled=True
                    settle_invest.save()
                    settle_invest.teammate.save()

                #设置为finished
                may_finish_bet.finished=True
                may_finish_bet.winner=winner
                may_finish_bet.score=score
                may_finish_bet.save()

    # 监控任务
    register_events(scheduler)
    # 调度器开始
    scheduler.start()
except Exception as e:
    print(e)
    # 报错则调度器停止执行
    scheduler.shutdown()

class MatchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = activity.models.Match.objects.all()
    serializer_class = activity.serializers.MatchSerializer
    filter_fields = ['tournament']
    ordering_fields = '__all__'

class InvestViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = activity.models.Invest.objects.all()
    serializer_class = activity.serializers.InvestSerializer
    filter_fields = ['id']
    ordering_fields = '__all__'

class MatchScheduler(views.APIView):
    authentication_classes=[]
    permission_classes = [permissions.AllowAny, ]

    def get(self, request, *args, **kwargs):
        scheduler=[]
        matches=activity.models.Match.objects.all()
        for match in matches:
            changed=False
            for cand in scheduler:
                # 可以看成是一次比赛的时间段
                if str(match.tournament)==str(cand["tournament"]):
                    if match.match_time>cand["start_time"]-timedelta(hours=16) and match.match_time<cand["end_time"]+timedelta(hours=16):
                        if cand["start_time"]==cand["end_time"]:
                            if match.match_time>cand["start_time"]:
                                cand["end_time"]=match.match_time
                            else:
                                cand["start_time"]=match.match_time
                        else:
                            if match.match_time<cand["start_time"]:
                                cand["start_time"]=match.match_time
                            elif match.match_time>cand["end_time"]:
                                cand["end_time"]=match.match_time

                        changed=True
                        break

            if not changed:
                scheduler.append({
                    "tournament":str(match.tournament),
                    "start_time":match.match_time,
                    "end_time":match.match_time,
                })

        return Response(scheduler)

class BetViewSet(viewsets.ModelViewSet):
    queryset = activity.models.Bet.objects.all()
    serializer_class=activity.serializers.BetSerializer

    @action(methods=['get'],detail=False,permission_classes=[permissions.AllowAny])
    def get_bets(self, request, *args, **kwargs):
        params = request.query_params
        num=int(params['sum'])
        rtn=[]
        if num==-1:
            bets=activity.models.Bet.objects.filter(finished=False).order_by("match_time")
        else:
            bets=activity.models.Bet.objects.filter(finished=False).order_by("match_time")[:num]
        for bet in bets:
            invests=activity.models.Invest.objects.filter(
                bet=bet
            )
            score_1=0
            score_2=0
            for invest in invests:
                if str(invest.target)==str(bet.player_1):
                    score_1+=int(invest.score)
                elif str(invest.target)==str(bet.player_2):
                    score_2+=int(invest.score)
            bet_1=0
            bet_2=0
            if score_1==0 and score_2==0:
                bet_1=0
                bet_2=0
            elif score_1==0 and score_2!=0:
                bet_1=0
                bet_2=1
            elif score_2==0 and score_1!=0:
                bet_2=0
                bet_1=1
            else:
                bet_1=round((score_1+score_2)/score_1,1)
                bet_2=round((score_1+score_2)/score_2,1)

            rtn.append({
                "id":bet.id,
                "player_1":bet.player_1,
                "player_2":bet.player_2,
                "tournament":bet.tournament,
                "match_url":bet.match_url,
                "time":bet.match_time,
                "stop_bet":bet.stop_bet,
                "finished":bet.finished,
                "bet_1":bet_1,
                "bet_2":bet_2
            })
        return Response(rtn)
    
    @action(methods=['get'],detail=False,permission_classes=[permissions.IsAuthenticated])
    def get_own_bets(self, request, *args, **kwargs):
        params = request.query_params
        rtn=[]
        user = request.user
        invests=activity.models.Invest.objects.filter(teammate=user.teammate).order_by("-bet")
        for invest in invests:
            bet=invest.bet
            ivs=activity.models.Invest.objects.filter(
                bet=bet
            )
            score_1=0
            score_2=0
            for iv in ivs:
                if str(iv.target)==str(bet.player_1):
                    score_1+=int(iv.score)
                elif str(iv.target)==str(bet.player_2):
                    score_2+=int(iv.score)
            bet_1=0
            bet_2=0
            if score_1==0 and score_2==0:
                bet_1=0
                bet_2=0
            elif score_1==0 and score_2!=0:
                bet_1=0
                bet_2=1
            elif score_2==0 and score_1!=0:
                bet_2=0
                bet_1=1
            else:
                bet_1=round((score_1+score_2)/score_1,1)
                bet_2=round((score_1+score_2)/score_2,1)

            rtn.append({
                "id":invest.id,
                "player_1":bet.player_1,
                "player_2":bet.player_2,
                "tournament":bet.tournament,
                "match_url":bet.match_url,
                "time":bet.match_time,
                "stop_bet":bet.stop_bet,
                "finished":bet.finished,
                "bet_1":bet_1,
                "bet_2":bet_2,
                "score":invest.score,
                "gain":invest.gain,
                "target":invest.target
            })          
        return Response(rtn)
    
    @action(methods=['post'],detail=False,permission_classes=[permissions.IsAuthenticated])
    def post_bet(self, request, *args, **kwargs):
        user = request.user
        serializer = activity.serializers.PostBetSerializer(
            data=request.data
        )
        if serializer.is_valid():
            if int(request.data['score'])<0 or int(request.data['score'])>int(user.teammate.score):
                return Response('Score format has error', 400)
            related_bet=activity.models.Bet.objects.get(id=request.data["bet_id"])
            if related_bet.stop_bet or related_bet.finished:
                return Response('Bet shut down', 400)
            activity.models.Invest.objects.create(
                score=request.data['score'],
                target=request.data['target'],
                teammate=user.teammate,
                bet=related_bet,
            )
            user.teammate.score=int(user.teammate.score)-int(request.data['score'])
            user.teammate.save()
            return Response('Bet success', 200)
        return Response('Serializer is invalid', 400)