from django.shortcuts import render
from rest_framework import generics
from .models import Company
from .serializers import CompanySerializer

# Create your views here.



class CompanyList(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer