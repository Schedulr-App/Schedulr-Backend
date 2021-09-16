from django.shortcuts import render
from rest_framework import generics
from .models import Company, Shift, Position
from .serializers import CompanySerializer, ShiftSerializer, PositionSerializer
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.models import User
import json

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

def user_list(request):
    users = User.objects.all().values('id', 'first_name','last_name','email','date_joined')
    users_list = users.filter(is_staff=False)
    return JsonResponse(list(users_list), safe=False)

def shift_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # Grabbing company
        companies = Company.objects.all().values('id', 'name')
        company = companies.filter(name=data['company'])
        companyId = company[0]['id']
        # Grabbing position
        positions = Position.objects.all().values('id', 'name')
        position = positions.filter(name=data['position'])
        positionId = position[0]['id']

        shift = Shift(company_id=companyId, title=data['title'], position_id=positionId, street=data['street'], city=data['city'], state=data['state'], zip=data['zip'], lat=data['lat'],lng=data['lng'], uniform=data['uniform'], description=data['description'], on_site_contact=data['on_site_contact'], meeting_location=data['meeting_location'], staff_needed=data['staff_needed'],payrate=data['payrate'], billrate=data['billrate'], start_time=data['start_time'], end_time=data['end_time'], created_by_id=1)

        shift.save()

        return HttpResponse('OK')
    else:
        HttpResponse('none')

def shift_update(request):
    if request.method == 'PUT':
        data = json.loads(request.body)

        shifts = Shift.objects.all()
        shift = shifts.filter(id=data['id'])
        print(shift)
        return HttpResponse('OK')
    else:
        pass