from channels.generic.websocket import AsyncWebsocketConsumer
from django.db import models
import json
from django.contrib.auth.models import User
from .models import RoomChatMessage, PrivateChatRoom, RoomChatMessageManager
from account.models import Account



class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.current_user = self.scope['user']
        user1_id = self.scope['user'].id
        user2_id = int(self.scope['url_route']['kwargs']['id'].replace(str(user1_id), ''))
        self.user1 = Account.objects.get(id=user1_id)
        self.user2 = Account.objects.get(id=user2_id)
        print(self.user1.username, self.user2.username)
        print(user1_id)
        

        RoomChatMessage.objects.get_or_create_private_chat(self.user1, self.user2)
        try:
            self.room_name_id = PrivateChatRoom.objects.get(user1=self.user1, user2=self.user2).id
            self.room = PrivateChatRoom.objects.get(user1=self.user1, user2=self.user2)
        except:
            self.room_name_id = PrivateChatRoom.objects.get(user1=self.user2, user2=self.user1).id
            self.room = PrivateChatRoom.objects.get(user1=self.user2, user2=self.user1)
        self.room_name = f'chat_{str(self.room_name_id)}'


        # Join room group
        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()


    async def disconnect(self, close_code):
        print('Disconnected')
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )
        
    # Receive message from WebSocket

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        self.message = text_data_json['message']
        print(self.message)
        print('Message has been recieved')
    
        await self.channel_layer.group_send(
            self.room_name,
            {
                'user1_username': self.user1.username,
                'user2_username': self.user2.username,
                'sender':  self.current_user.id, 
                'type': 'chat_message',
                'message': self.message,
                
            }
        )
        # Saving a message in a database
        RoomChatMessage.objects.create(
            user = self.current_user,
            room = self.room,
            content= self.message
        )

    # Receive message from room group
    async def chat_message(self, event):
        print('message has been sent')
        self.message = event['message']
        print(event)
        print(f'event sender = {event["sender"]}' )

        # Send message to WebSocket
        await self.send(text_data=json.dumps({

            'message': self.message,
            'sender' : event['sender'],
            'user1_username': self.user1.username,
            'user2_username': self.user2.username,
        }))

    