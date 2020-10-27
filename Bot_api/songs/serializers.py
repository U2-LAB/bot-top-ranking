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
    
    def create(self, validated_data):
        songs_data = validated_data.pop('songs')
        poll = Poll.objects.create(**validated_data)
        for song_data in songs_data:
            Song.objects.create(poll=poll, **song_data)
        return poll


class ChatSerializer(serializers.ModelSerializer):
    polls = PollSerializer(many=True, required=False)

    class Meta:
        model = Chat
        fields = ['id','telegram_chat_id', 'polls']

    def create(self, validated_data):
        polls_data = validated_data.pop('polls')
        chat = Chat.objects.create(**validated_data)
        for poll_data in polls_data:
            Poll.objects.create(chat=chat, **poll_data)
        return chat
