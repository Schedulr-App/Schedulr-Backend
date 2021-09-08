from re import T
from rest_framework import serializers
from .models import Company, Shift, Position

class CompanySerializer(serializers.ModelSerializer):
    shifts = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    class Meta:
        model = Company
        fields = ('id', 'name', 'contact_name', 'contact_email', 'contact_phone', 'contact_position', 'shifts')
        depth = 1

class ShiftSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    position = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    staff_claimed = serializers.PrimaryKeyRelatedField(
        # view_name='companies_detail',
        many=True,
        read_only=True
    )
    created_by = serializers.PrimaryKeyRelatedField(
        read_only=True
    )
    class Meta:
        model = Shift
        fields = ('id', 'company', 'title', 'position', 'street', 'city', 'state', 'zip', 'lat', 'lng', 'uniform', 'description', 'on_site_contact', 'meeting_location', 'staff_needed', 'staff_claimed', 'start_time', 'end_time', 'payrate', 'billrate', 'created_at', 'created_by')
        depth = 1
