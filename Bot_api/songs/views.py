from rest_framework import generics

from .models import Chat, Poll, Song
from .serializers import ChatSerializer, PollSerializer, SongSerializer


class ChatDetail(generics.RetrieveUpdateDestroyAPIView,generics.CreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ChatList(generics.ListAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

class PollDetail(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class SongList(generics.ListAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

class SongDetail(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)        