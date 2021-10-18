from django.shortcuts import render
from rest_framework import generics
from .models import Company, Shift, Position
from .serializers import CompanySerializer, ShiftSerializer, PositionSerializer
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.models import User
import json
import csv
import datetime
from django.utils import timezone


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
    shifts_list = list(shifts)
    processed = {}
    for record in shifts_list:
        if record['id'] in processed.keys():
            processed[record['id']]['staff_count'] += 1
            processed[record['id']]['staff_array'].append(record['staff_claimed'])
        else:
            temp = record
            if temp['staff_claimed']:
                temp['staff_count'] = 1
            else:
                temp['staff_count'] = 0
            temp['staff_array'] = [record['staff_claimed']]
            processed[record['id']] = temp

    return JsonResponse(processed, safe=False)

def shift_detail(request, pk):
    shift = Shift.objects.filter(id=pk)
    shift.select_related('staff_claimed')
    shift_detail = shift.values('id', 'company', 'title', 'position', 'street', 'city', 'state', 'zip', 'lat', 'lng', 'uniform', 'description', 'on_site_contact', 'meeting_location', 'staff_needed', 'staff_claimed', 'payrate', 'billrate', 'start_time', 'end_time', 'created_at', 'created_by', 'company__name', 'staff_claimed__first_name', 'staff_claimed__last_name', 'staff_claimed__id')
    shifts_list = list(shift_detail)
    processed = {}
    for record in shifts_list:
        if record['id'] in processed.keys():
            processed[record['id']]['staff_count'] += 1
            processed[record['id']]['staff_array'].append(record['staff_claimed'])
            processed[record['id']]['staff_info'].append({ 'id': record['staff_claimed__id'], 'firstname': record['staff_claimed__first_name'], 'lastname': record['staff_claimed__last_name']})
        else:
            temp = record
            temp['staff_count'] = 1
            temp['staff_array'] = [record['staff_claimed']]
            temp['staff_info'] = [{ 'id': record['staff_claimed__id'], 'firstname': record['staff_claimed__first_name'], 'lastname': record['staff_claimed__last_name']}]
            processed[record['id']] = temp

            
    return JsonResponse(processed, safe=False)

def user_list(request):
    users = User.objects.all().values('id', 'first_name','last_name','email','date_joined')
    users_list = users.filter(is_staff=False)
    return JsonResponse(list(users_list), safe=False)

# Creating Shift from front-end and configuring position and company
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

        return HttpResponse('Your request has been received')
    else:
        HttpResponse('Something went wrong')

#Updating shift from front-end
def shift_update(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        shifts = Shift.objects.all()
        shifts.filter(id=data['id']).update(title=data['title'], street=data['street'], city=data['city'], state=data['state'], zip=data['zip'], lat=data['lat'],lng=data['lng'], uniform=data['uniform'], description=data['description'], on_site_contact=data['on_site_contact'], meeting_location=data['meeting_location'],payrate=data['payrate'], billrate=data['billrate'], start_time=data['start_time'], end_time=data['end_time'])
        return HttpResponse('Success, the shift has been updated.')
    else:
        HttpResponse('Something went wrong')

def shift_assign(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        shift = Shift.objects.get(id=data['shift_id']) 
        print(shift.staff_claimed)
        # shifts_list=list(shift)
        # processed = {}
        # for record in shifts_list:
        #     if record['id'] in processed.keys():
        #         processed[record['id']]['staff_count'] += 1
        #         processed[record['id']]['staff_array'].append(record['staff_claimed'])
        #     else:
        #         temp = record
        #         if temp['staff_claimed']:
        #             temp['staff_count'] = 1
        #         else:
        #             temp['staff_count'] = 0
        #         temp['staff_array'] = [record['staff_claimed']]
        #         processed[record['id']] = temp
        # print(processed)
        worker = User.objects.get(id=data['user'])
        shift.staff_claimed.add(worker)
        return HttpResponse('Your request has been received')
    else:
        HttpResponse('Something went wrong')

def shift_remove(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        shift = Shift.objects.get(id=data['shift_id'])
        worker =User.objects.get(id=data['user'])
        shift.staff_claimed.remove(worker)
        return HttpResponse('Your request has been received')
    else:
        HttpResponse('Something went wrong')

def user_create(request):
    if request.method=='POST':
        data = json.loads(request.body)
        worker = User.objects.create_user(username=data['username'], first_name=data['first_name'], last_name=data['last_name'], email=data['email'])
        worker.save()
        return HttpResponse('Your request has been received')
    else:
        HttpResponse('Something went wrong')

def user_detail(request, pk):
    user = User.objects.filter(id=pk)
    user_detail = user.values('id', 'email', 'first_name', 'last_name', 'username')
    return JsonResponse(list(user_detail), safe=False)


## Exporting Data

def shift_export(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['Shift Id', 'Shift Title', 'Company Id', 'Company Name', 'Position Id', 'Position Name', 'Street Address', 'City', 'State', 'Zip Code', 'Latitude', 'Longitude', 'Uniform', 'Description', 'Onsite Contact', 'Meeting Location', 'Staff Needed', 'Staff Id', 'Staff First Name', 'Staff Last Name', 'Payrate', 'Billrate', 'Start Time', 'End Time', 'Created At', 'Created By'])

    for shift in Shift.objects.all().values_list('id', 'title', 'company', 'company__name', 'position', 'position__name', 'street', 'city', 'state', 'zip', 'lat', 'lng', 'uniform', 'description', 'on_site_contact', 'meeting_location', 'staff_needed', 'staff_claimed', 'staff_claimed__first_name', 'staff_claimed__last_name', 'payrate', 'billrate', 'start_time', 'end_time', 'created_at', 'created_by', ):
        writer.writerow(shift)
    
    response['Content-Disposition'] = 'attachment; filename="shifts.csv"'

    return response


## Data Vis Return

def shift_visual(request):
    shifts = shifts = Shift.objects.all()
    shiftsPast = shifts.filter(start_time__lte=timezone.now())
    pastSeven = shiftsPast.filter(start_time__gte=timezone.now() - datetime.timedelta(days=7))
    shiftList = pastSeven.values('id', 'company', 'title', 'position', 'street', 'city', 'state', 'zip', 'lat', 'lng', 'uniform', 'description', 'on_site_contact', 'meeting_location', 'staff_needed', 'staff_claimed', 'payrate', 'billrate', 'start_time', 'end_time', 'created_at', 'created_by', 'company__name')
    shiftCount = 0
    for record in pastSeven:
        shiftCount += 1
    print(shiftList)
    return JsonResponse(shiftCount, safe=False)
