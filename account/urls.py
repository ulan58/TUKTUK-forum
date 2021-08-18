from django.urls import path

from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('activate/<str:email>/<str:activation_code>', ActivationView.as_view(), name='activate'),
]