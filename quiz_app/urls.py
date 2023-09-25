from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quiz/<int:quiz_id>/', views.quiz, name='quiz'),
    path('results/<int:quiz_id>/', views.results, name='results'),
]
