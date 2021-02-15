from django.urls import path

from .views import displaying_messages, select_chat_room

urlpatterns = [
    path('<str:room_name>/', displaying_messages, name='room'),
    path('', select_chat_room, name='select_chat_room')
]