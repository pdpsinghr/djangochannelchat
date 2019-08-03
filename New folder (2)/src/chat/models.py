# from djangotoolbox.fields import *
from django.db import models
from mongoengine import *
connect('chat')

# Create your models here.
class Chat(models.Model):
    author = models.TextField()
    message = models.TextField()
    chatRoom = models.TextField()