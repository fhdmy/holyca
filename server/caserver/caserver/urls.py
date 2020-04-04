from django.contrib import admin
from django.conf.urls import url, include
from rest_framework import routers
import account.views
import match.views

accountRouter = routers.DefaultRouter()
accountRouter.register(r'teammates', account.views.TeammateViewSet)
accountRouter.register(r'users', account.views.UserViewSet)
accountRouter.register(r'repstats', account.views.RepStatsViewSet)

matchRouter=routers.DefaultRouter()
matchRouter.register(r'mmr', match.views.MMRViewSet)
matchRouter.register(r'replay', match.views.ReplayViewSet)
matchRouter.register(r'battlenet_account', match.views.BattlenetAccountViewSet)

base_urlpatterns= [
    url(r'^account/', include(accountRouter.urls)),
    url(r'^account/sign_up/$', account.views.SignUp.as_view(), name='sign-up'),

    url(r'^match/', include(matchRouter.urls)),
    url(r'^match/active_statistics/$', match.views.ActiveStatistics.as_view(), name='active-statistics'),
    url(r'^match/replay_statistics/$', match.views.ReplayStatistics.as_view(), name='replay-statistics'),
    url(r'^match/mmr_statistics/$', match.views.MMRStatistics.as_view(), name='mmr-statistics'),
    url(r'^match/racesum_statistics/$', match.views.RaceSumStatistics.as_view(), name='racesum-statistics'),
    url(r'^match/race_winrate_statistics/$', match.views.RaceWinrateStatistics.as_view(), name='race-winrate-statistics'),
]

urlpatterns = [
    url(r'^api/', include(base_urlpatterns)),
]
