from django.shortcuts import render

from rest_framework import viewsets

from .models import Messagefromsky
from .serializers import MessageSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Messagefromsky.objects.all().filter(seen='False')
    serializer_class = MessageSerializer
