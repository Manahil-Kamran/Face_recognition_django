from rest_framework import serializers
from dashboard.models import PersonRegistration, FaceCoding

class PersonRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonRegistration
        fields = '__all__'

class FaceCodingSerializer(serializers.ModelSerializer):
    person_id=serializers.CharField(source="person.id")
    person_name=serializers.CharField(source="person.full_name")
    department_name=serializers.CharField(source="person.department_name")
    class Meta:
        model = FaceCoding
        fields = ["person_id","person_name","department_name","face_feature"]


