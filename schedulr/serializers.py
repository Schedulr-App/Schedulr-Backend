from rest_framework import serializers
from .models import Company, Shift, Position

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name', 'contact_name', 'contact_email', 'contact_phone', 'contact_position')
