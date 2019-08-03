# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client['chat']
chatData = db.chat_chat 
import json


class ChatConsumer(AsyncWebsocketConsumer):
    # def fetch_messages(self):
    #     chats = Chat.objects.all() 


    async def connect(self):
        arr = []
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # data = db.chat_chat.find()
        # for d in data:
        #     arr.append(d)
        #     print(arr)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        self.send(arr)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        self.room_name = self.scope['url_route']['kwargs']['room_name']

        chat = Chat.objects.create(
            author=username,
            message= message,
            chatRoom=self.room_name
        )
        chat.save()
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        # print('event', event)
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))