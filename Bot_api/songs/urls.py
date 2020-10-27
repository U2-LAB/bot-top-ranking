from django.urls import path

from .views import ChatDetail, ChatList, PollDetail, SongList, SongDetail

app_name = 'chats'

urlpatterns = [
    path('chat/<int:pk>', ChatDetail.as_view()),
    path('chat/', ChatList.as_view()),
    path('poll/<int:pk>', PollDetail.as_view()),
    path('song/', SongList.as_view()),
    path('song/<int:pk>', SongDetail.as_view()),
]

# curl example
# POST example
# curl --data "telegram_chat_id=0330" http://127.0.0.1:8000/api/chat/1
# curl --data "poll_telegram_id=23&chat_id=3" http://127.0.0.1:8000/api/poll/1
# curl --data "poll_id=3&title=qwertyyuiop&mark=5" http://127.0.0.1:8000/api/song/1
# DELETE example
# curl -X DELETE http://127.0.0.1:8000/api/chat/3
# PUT example
# curl -X PUT -d telegram_chat_id=789 http://127.0.0.1:8000/api/chat/4