from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Note
from .serializers import NoteSerializer
from rest_framework import status
from django.shortcuts import render
import json 
from django.http import HttpResponse

# from django.http import HttpResponse

# Create your views here.

# class getUsers(APIView):
#     def get(self, request, format=None):
#         note = Note.objects.all()
#         ser = NoteSerializer(note, many=True)
#         print("req received")
#         return Response(ser.data)
    
#     def post(self, request, format=None):
#         serializer = NoteSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

score = {}

@api_view(['GET'])
def getDashboardScores(request):
    global score
    score = {
        "google": {
            "ml": 70,
            "wd": 30
        },
        "youtube": {
            "ml": 40,
            "wd": 60
        }
    }
    return Response(score, status=status.HTTP_200_OK)

@api_view(['POST'])
def getHistoryAnalysis(request):
    # print("can see", request.data)
    return Response(status=status.HTTP_200_OK)

