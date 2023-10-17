from django.http import HttpResponse
from rest_framework import viewsets
#from .serializers import ModelSerializer
#from .models import Model

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the API.")

#class ModelView(viewsets.ModelViewSet):
#    serializer_class = ModelSerializer
#    queryset = Model.objects.all()