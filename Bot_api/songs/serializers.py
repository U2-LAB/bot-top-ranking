from .models import Chat, Poll, Song
from rest_framework import serializers


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'title', 'mark', 'poll_id']


class PollSerializer(serializers.ModelSerializer):
    songs = SongSerializer(many=True, required=False)

    class Meta:
        model = Poll
        fields = ['poll_id', 'songs', 'chat_id']


class ChatSerializer(serializers.ModelSerializer):
    polls = PollSerializer(many=True, required=False)

    class Meta:
        model = Chat
        fields = ['chat_id', 'polls']
