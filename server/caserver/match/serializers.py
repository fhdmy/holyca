from rest_framework import serializers
import match.models

class MMRSerializer(serializers.ModelSerializer):
    class Meta:
        model = match.models.MMR
        fields = '__all__'

class ReplaySerializer(serializers.ModelSerializer):
    class Meta:
        model = match.models.Replay
        fields = '__all__'

class BattlenetAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = match.models.BattlenetAccount
        fields = '__all__'

class RecentReplaySerializer(serializers.ModelSerializer):
    class BNSerializer(serializers.ModelSerializer):
        class Meta:
            model = match.models.BattlenetAccount
            fields = ['battlenet_name', 'battlenet_id']

    player1 = BNSerializer(read_only=True)
    player2 = BNSerializer(read_only=True)
    class Meta:
        model = match.models.Replay
        fields = ['rep_id','player1_mmr','player2_mmr','winner','date','vs_race','game_length','game_map','player1','player2']