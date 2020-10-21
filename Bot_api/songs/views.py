from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Chat
from .serializers import ChatSerializer


class ChatView(APIView):
    def get(self, request):
        chats = Chat.objects.all()

        serializer = ChatSerializer(chats, many=True)
        return Response({'chats': serializer.data})
