
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EmailClassificationRequestSerializer, EmailClassificationResponseSerializer

from transformers import BertTokenizer, TFBertForSequenceClassification
import tensorflow as tf
import os
import numpy as np  


MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models', 'email_span_model')
print(f"Attempting to load model from path: {MODEL_PATH}")

tokenizer = None 
model = None

try:
    
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    #trained model from the saved directory

    model = TFBertForSequenceClassification.from_pretrained(MODEL_PATH)
    print("BERT model and tokenizer loaded successfully!") 
except Exception as e:
    print(f"Error loading BERT model or tokenizer: {e}")
    
def predict_spam(text, model, tokenizer):
    inputs = tokenizer(text, truncation=True, padding=True, return_tensors='tf')
    outputs = model(inputs)
    logits = outputs.logits
    probabilities = tf.nn.softmax(logits, axis=-1).numpy()[0]
    predicted_class = np.argmax(probabilities)
    return predicted_class, probabilities


class ClassifyEmailAPIView(APIView):
    def post(self, request, *args, **kwargs):
        """
        Endpoint to classify email text as spam or not spam using the BERT model.
        Accepts email_text in the request body and returns a prediction.
        """

        if not tokenizer or not model: 
            return Response(
                {"error": "Model loading failed. Please check server logs for startup errors."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        serializer = EmailClassificationRequestSerializer(data=request.data) # Validate input data
        if serializer.is_valid():
            email_text = serializer.validated_data['email_text']

            # --- Make prediction using the predict_spam function ---
            try:
                predicted_class, probabilities = predict_spam(email_text, model, tokenizer)

                response_data = {
                    'predicted_class': int(predicted_class),  
                    'probabilities': probabilities.tolist()   
                }
                response_serializer = EmailClassificationResponseSerializer(response_data) 

                return Response(response_serializer.data, status=status.HTTP_200_OK)

            except Exception as prediction_error:
                print(f"Prediction error: {prediction_error}") 
                return Response(
                    {"error": "Error during prediction. Please check server logs."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        else:
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        