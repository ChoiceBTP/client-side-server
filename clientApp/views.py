from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Note
from .serializers import NoteSerializer
from rest_framework import status
from django.shortcuts import render
import json 
from django.http import HttpResponse
import requests, json
from django.conf import settings
from django.core.mail import send_mail

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

from .mlModel import Inferrer
inf = Inferrer()

score = {}
domain = "Machine Learning"

class SummaryReport:
    total_score = 0

    def compute_total_score():
        global score
        topic_freq = {}
        for ele in score:
            topic_freq[score[ele]] = topic_freq.get(score[ele], 0) + 1

        SummaryReport.toal_score = (topic_freq.get(domain, 0)/len(score))*100;

    def mail_summary_report(self):
        response = requests.get('http://localhost:3333/getHistory?time=13312950000000000')
        json_data = json.loads(response.text)
        classes = json_data["classes"]
        ind = 0
        class_freq = {}
        for ele in json_data["urls_list"]:
            class_freq[ele] = classes[ind]
            ind += 1
        global score
        score = class_freq

        SummaryReport.compute_total_score()

        subject = "Daily report of choice app"
        message = ""
        if(SummaryReport.total_score>60):
            message = "Keep it Up! you are close to achieve your goal"
        elif(SummaryReport.total_score > 10):
            message = "You need to focus more on your task to achieve your goal"
        else:
            message = "You haven't made any progress yet. start working"

        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['saurav.mc19@nsut.ac.in', 'harshit.co19@nsut.ac.in', 'tanmay.cs19@nsut.ac.in']
        send_mail(subject, message, email_from, recipient_list)
        print('MAIL SENT')
        return

@api_view(['GET'])
def getDashboardScores(request):
    global score
    print("send dashoard scores ", score)
    return Response(score, status=status.HTTP_200_OK)

@api_view(['POST'])
def getHistoryAnalysis(request):
    global domain
    domain = request.data['domain']
    print("can see", request.data)
    response = requests.get('http://localhost:3333/getHistory?time=13312950000000000')
    json_data = json.loads(response.text)
    classes = json_data["classes"]
    print("response ", classes, json_data["urls_list"])
    ind = 0
    class_freq = {}
    for ele in json_data["urls_list"]:
        class_freq[ele] = classes[ind]
        ind += 1
    global score
    score = class_freq
    return Response(status=status.HTTP_200_OK)

@api_view(['POST'])
def getChatResponse(request):
    print("got a request")
    # input_string = requests.data["input_string"]  # assuming the request is in JSON format

    # print(input_string)
    received_json_data=json.loads(request.body)
    input_string = received_json_data["input_string"]
    output_string = inf.model_response(input_string)
    print(output_string)
    # Process the input string and generate the response
    # response =
    # print(response)
    return Response({'message': output_string}, status=status.HTTP_200_OK)

