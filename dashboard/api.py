from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from dashboard.models import PersonRegistration
from dashboard.serializers import PersonRegistrationSerializer

class GetFaceCodingApiView(APIView):
    def get(self, request):
        # Assuming `model_classes` is a list of person IDs you're filtering on
        records = PersonRegistration.objects.filter(
            facecoding__is_current=True  # Equivalent to `Face_Coding.is_current == 1`
        )
        serialized_records = PersonRegistrationSerializer(records, many=True)
        return Response(serialized_records.data, status=status.HTTP_200_OK)
