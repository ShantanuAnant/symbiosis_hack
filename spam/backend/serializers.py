# classifier_app/serializers.py
from rest_framework import serializers

class EmailClassificationRequestSerializer(serializers.Serializer):
    email_text = serializers.CharField()

class EmailClassificationResponseSerializer(serializers.Serializer):
    predicted_class = serializers.IntegerField()  # Use IntegerField for predicted_class (0 or 1)
    probabilities = serializers.ListField(child=serializers.FloatField()) # List of floats for probabilities
    # Now it matches the keys in your response_data in views.py