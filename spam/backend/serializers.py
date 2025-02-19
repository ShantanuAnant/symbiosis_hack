# classifier_app/serializers.py
from rest_framework import serializers

class EmailClassificationRequestSerializer(serializers.Serializer):
    email_text = serializers.CharField()

class EmailClassificationResponseSerializer(serializers.Serializer):
    predicted_class = serializers.IntegerField()  
    probabilities = serializers.ListField(child=serializers.FloatField())
    