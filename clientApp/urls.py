from django.urls import path

from . import views

urlpatterns = [
    path('data/', views.getHistoryAnalysis, name="history-analysis"),
    path('score/', views.getDashboardScores, name="dashboard-scores"),
    path('getPred/', views.getChatResponse, name="chat-response")
]