# classifier_app/urls.py
from django.urls import path
from .views import ClassifyEmailAPIView 

urlpatterns = [
    path('classify_email_api/', ClassifyEmailAPIView.as_view(), name='classify_email_api'), 
]