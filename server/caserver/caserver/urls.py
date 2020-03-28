from django.contrib import admin
from django.conf.urls import url, include
from rest_framework import routers
import account.views

accountRouter = routers.DefaultRouter()
accountRouter.register(r'teammates', account.views.TeammateViewSet)
accountRouter.register(r'users', account.views.UserViewSet)

base_urlpatterns= [
    url(r'^account/', include(accountRouter.urls)),
    url(r'^account/sign_up/$', account.views.SignUp.as_view(), name='sign-up'),
]

urlpatterns = [
    url(r'^api/', include(base_urlpatterns)),
]
