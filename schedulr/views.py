from django.shortcuts import render
from rest_framework import generics
from .models import Company, Shift, Position, Location
from .serializers import CompanySerializer, PositionSerializer
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth.models import User
import json
import csv
import datetime
from django.utils import timezone


## Views ##

# Class based serailizers

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


## Function based ##

# Returning all shift detail
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


# Returning shift detail about requested shift
def shift_detail(request, pk):
    shift = Shift.objects.filter(id=pk)
    shift.select_related('staff_claimed')
    shift_detail = shift.values('id', 'company', 'title', 'position', 'street', 'city', 'state', 'zip', 'lat', 'lng', 'uniform', 'description', 'on_site_contact', 'meeting_location', 'staff_needed', 'staff_claimed', 'payrate', 'billrate', 'start_time', 'end_time', 'created_at', 'created_by', 'company__name', 'staff_claimed__first_name', 'staff_claimed__last_name', 'staff_claimed__id', 'full', 'closed')
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

# Returning all staff accounts
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

# Updating shift from front-end
def shift_update(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        shifts = Shift.objects.all()
        shifts.filter(id=data['id']).update(title=data['title'], street=data['street'], city=data['city'], state=data['state'], zip=data['zip'], lat=data['lat'],lng=data['lng'], uniform=data['uniform'], description=data['description'], on_site_contact=data['on_site_contact'], meeting_location=data['meeting_location'],payrate=data['payrate'], billrate=data['billrate'], start_time=data['start_time'], end_time=data['end_time'])
        return HttpResponse('Success, the shift has been updated.')
    else:
        HttpResponse('Something went wrong')

# Returning unassigned staff for the selected shift record
def shift_available_staff(request, pk):
    shift = Shift.objects.filter(id=pk)
    shift_claim_detail = shift.values('staff_claimed')
    staff = User.objects.all().values('id', 'first_name','last_name')
    staff_list = list(staff)
    print('Staff List')
    print(staff_list)
    worker_list = []

    for staff in staff_list:
        worker_list.append(staff['id'])

    for claim in shift_claim_detail:
        if claim['staff_claimed'] in worker_list:
            worker_list.remove(claim)

    return HttpResponse('Request Received')

# Assigning staff to shift
def shift_assign(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        shift = Shift.objects.get(id=data['shift_id'])
        claimList = shift.staff_claimed.values()
        needed = shift.staff_needed
        claimed = 0

        for record in claimList:
            claimed += 1

        worker = User.objects.get(id=data['user'])

        if claimed >= needed:
            return HttpResponse('The shift is full, please review the staff list', status=250)
        
        else: 
            shift.staff_claimed.add(worker)
            claimed += 1
            if claimed == needed:
                shift.full = True
                shift.save()
            return HttpResponse('Your request has been received')
            

    else:
        HttpResponse('Something went wrong')

# Removing staff from shift
def shift_remove(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        shift = Shift.objects.get(id=data['shift_id'])
        worker =User.objects.get(id=data['user'])
        shift.staff_claimed.remove(worker)
        if shift.full:
            shift.full = False
            shift.save()
        return HttpResponse('Your request has been received')
    else:
        HttpResponse('Something went wrong')

# Creating new staff account
def user_create(request):
    if request.method=='POST':
        data = json.loads(request.body)
        worker = User.objects.create_user(username=data['username'], first_name=data['first_name'], last_name=data['last_name'], email=data['email'])
        worker.save()
        return HttpResponse('Your request has been received')
    else:
        HttpResponse('Something went wrong')

# Returning staff details about requested staff record
def user_detail(request, pk):
    user = User.objects.filter(id=pk)
    user_detail = user.values('id', 'email', 'first_name', 'last_name', 'username')
    return JsonResponse(list(user_detail), safe=False)

# Returning locations from database
def location_list(request):
    location = Location.objects.all().values('name', 'street', 'city', 'state', 'zip')
    return JsonResponse(list(location), safe=False)

# Create new location to database
def location_create(request):
    if request.method == 'POST':

        data = json.loads(request.body)

        print(data)

        location = Location(name=data['name'], street=data['street'], city=data['city'], state=data['state'], zip=data['zip'], lat=data['lat'],lng=data['lng'])

        location.save()

        return HttpResponse('Your request has been received')
    else:
        HttpResponse('Something went wrong')

## Exporting Data Responses ##

# Returning all shift data
def shift_export(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)
    writer.writerow(['Shift Id', 'Shift Title', 'Company Id', 'Company Name', 'Position Id', 'Position Name', 'Street Address', 'City', 'State', 'Zip Code', 'Latitude', 'Longitude', 'Uniform', 'Description', 'Onsite Contact', 'Meeting Location', 'Staff Needed', 'Staff Id', 'Staff First Name', 'Staff Last Name', 'Payrate', 'Billrate', 'Start Time', 'End Time', 'Created At', 'Created By'])

    for shift in Shift.objects.all().values_list('id', 'title', 'company', 'company__name', 'position', 'position__name', 'street', 'city', 'state', 'zip', 'lat', 'lng', 'uniform', 'description', 'on_site_contact', 'meeting_location', 'staff_needed', 'staff_claimed', 'staff_claimed__first_name', 'staff_claimed__last_name', 'payrate', 'billrate', 'start_time', 'end_time', 'created_at', 'created_by', ):
        writer.writerow(shift)
    
    response['Content-Disposition'] = 'attachment; filename="shifts.csv"'

    return response

def staff_export(request):
    response = HttpResponse(content_type='text/csv')

    writer = csv.writer(response)

    writer.writerow(['Worker Id', 'First Name', 'Last Name', 'Email', 'Created Date'])
    users = User.objects.all().values('id', 'first_name','last_name','email','date_joined')
    users_list = User.objects.filter(is_staff=False)

    for user in users_list.values_list('id', 'first_name','last_name','email','date_joined'):
        writer.writerow(user)
    
    response['Content-Disposition'] = 'attachment; filename="staff_list.csv"'

    return response


## Data Visual Responses ##

# Returns number of shifts which occured in 3 historical timeframes
def shift_visual(request):
    shifts = Shift.objects.all()
    shiftsPast = shifts.filter(start_time__lte=timezone.now())
    shiftList = shifts.values('id', 'company', 'title', 'position', 'street', 'city', 'state', 'zip', 'lat', 'lng', 'uniform', 'description', 'on_site_contact', 'meeting_location', 'staff_needed', 'staff_claimed', 'payrate', 'billrate', 'start_time', 'end_time', 'created_at', 'created_by', 'company__name')

    pastSeven = shiftList.filter(start_time__gte=timezone.now() - datetime.timedelta(days=7))
    pastTwoWeek = shiftList.filter(start_time__gte=timezone.now() - datetime.timedelta(days=14))
    pastMonth = shiftList.filter(start_time__gte=timezone.now() - datetime.timedelta(days=30))
    
    shiftCount = {
        'weekCount': 0,
        'twoWeekCount': 0,
        'monthCount': 0,
    }

    for record in pastSeven:
        shiftCount['weekCount'] += 1
    
    for record in pastTwoWeek:
        shiftCount['twoWeekCount'] += 1
    
    for record in pastMonth:
        shiftCount['monthCount'] += 1

    return JsonResponse(shiftCount, safe=False)

# Returns fill rate of all shifts
def fillrate_visual(request):
    shifts = Shift.objects.all()
    kind = {
        'full': 0,
        'open': 0,
        'total':0,
    }
    for record in shifts:
        if record.full:
            kind['full'] += 1
            kind['total'] += 1
        else:
            kind['open'] += 1
            kind['total'] += 1
    return JsonResponse(kind, safe=False)

    
