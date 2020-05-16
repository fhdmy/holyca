from rest_framework import serializers
import activity.models

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = activity.models.Match
        fields = '__all__'


class BetSerializer(serializers.ModelSerializer):
    class Meta:
        model = activity.models.Bet
        fields = '__all__'

class InvestSerializer(serializers.ModelSerializer):
    class Meta:
        model = activity.models.Invest
        fields = '__all__'

class PostBetSerializer(serializers.Serializer):
    score = serializers.IntegerField()
    target = serializers.CharField()
    bet_id = serializers.IntegerField()