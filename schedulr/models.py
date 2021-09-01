from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import SET_DEFAULT

# Create your models here.

#### Company Model

class Company(models.Model):
    name = models.CharField(max_length=100)
    contact_name = models.CharField(max_length=100)
    contact_email = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=10)
    contact_position = models.CharField(max_length=100)

    def __str__(self):
        return self.name

#### Position Model

class Position(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

#### Shift Model
class Shift(models.Model):
    company = models.ForeignKey(
        Company,
        default='Company',
        on_delete=SET_DEFAULT, 
        related_name='shift_company'
    )
    title  = models.CharField(max_length=100)
    position = models.ForeignKey(
        Position,
        related_name='shift_position',
        default='Position',
        on_delete=SET_DEFAULT
    )
    address = models.CharField(max_length=200)
    uniform = models.TextField()
    description = models.TextField()
    on_site_contact = models.CharField(max_length=100)
    meeting_location = models.CharField(max_length=200)
    staff_needed = models.IntegerField()
    staff_claimed = models.ManyToManyField(
        User,
        related_name='shift_claims',
        default='Worker',
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, 
        default='Admin',
        on_delete=SET_DEFAULT, 
        related_name='shift_admin'
    )
    def __str__(self):
        return self.title

