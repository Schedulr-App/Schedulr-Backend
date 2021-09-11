from django.shortcuts import render
from rest_framework import generics
from .models import Company, Shift, Position
from .serializers import CompanySerializer, ShiftSerializer, PositionSerializer
from django.http import JsonResponse

# Create your views here.



class CompanyList(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class CompanyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class PositionList(generics.ListCreateAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

class PositionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

# class ShiftList(generics.ListCreateAPIView):
#     queryset = Shift.objects.all()
#     serializer_class = ShiftSerializer

# class ShiftDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Shift.objects.all()
#     serializer_class = ShiftSerializer

def shift_list(request):
    shifts = Shift.objects.all().values('id', 'company', 'title', 'position', 'street', 'city', 'state', 'zip', 'lat', 'lng', 'uniform', 'description', 'on_site_contact', 'meeting_location', 'staff_needed', 'staff_claimed', 'payrate', 'billrate', 'start_time', 'end_time', 'created_at', 'created_by', 'company__name')
    companies = Company.objects.all().values('id','name','contact_name', 'contact_email', 'contact_phone', 'contact_position' )
    shifts_list = list(shifts)
    return JsonResponse(shifts_list, safe=False)

def shift_detail(request, pk):
    shifts = Shift.objects.all().values('id', 'company', 'title', 'position', 'street', 'city', 'state', 'zip', 'lat', 'lng', 'uniform', 'description', 'on_site_contact', 'meeting_location', 'staff_needed', 'staff_claimed', 'payrate', 'billrate', 'start_time', 'end_time', 'created_at', 'created_by', 'company__name')
    shift = shifts.filter(id=pk)
    return JsonResponse(list(shift), safe=False)