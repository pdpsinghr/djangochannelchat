# chat/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017')
db = client['chat']
chatData = db.chat_chat 
import json


def index(request):
    return render(request, 'chat/index.html', {}) 


def room(request, room_name):
    array = []
    data = db.chat_chat.find()
    for d in data:
        arr = []
        arr.append(d['author'])
        arr.append(d['message'])
        array.append(arr)
        print(arr)
    print('request', request.user)
    return render(request, 'chat/room.html', {
        'old_messages': mark_safe(json.dumps(array)),
        'room_name_json': mark_safe(json.dumps(room_name))
    })