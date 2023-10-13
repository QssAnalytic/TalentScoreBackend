from rest_framework.views import APIView
from users.models import Country
from rest_framework.response import Response


class GetCountrysAPIView(APIView):
    def get(self, request):
        countries = Country.objects.values("name")
        
        return Response(countries)