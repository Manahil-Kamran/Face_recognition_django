from rest_framework import serializers
from dashboard.models import PersonRegistration, FaceCoding

class PersonRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonRegistration
        fields = '__all__'

class FaceCodingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaceCoding
        fields = '__all__'
