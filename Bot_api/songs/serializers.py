from .models import Chat, Poll, Song
from rest_framework import serializers


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'poll_id', 'title', 'mark', ]


class PollSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True, required=False)

    class Meta:
        model = Poll
        fields = ['id','poll_telegram_id', 'chat_id', 'songs', ]


class ChatSerializer(serializers.ModelSerializer):
    polls = PollSerializer(many=True, required=False)

    class Meta:
        model = Chat
        fields = ['id','telegram_chat_id', 'polls']
