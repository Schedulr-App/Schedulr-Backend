from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import SET, SET_DEFAULT, CASCADE
# from .models import Shift

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
        related_name='shifts'
    )
    title  = models.CharField(max_length=100)
    position = models.ForeignKey(
        Position,
        related_name='shift_position',
        default='Position',
        on_delete=SET_DEFAULT
    )
    street = models.CharField(max_length=200, default='null')
    city = models.CharField(max_length=100, default='null')
    state = models.CharField(max_length=2, default='NA')
    zip = models.CharField(max_length=5, default='null')
    lat = models.CharField(max_length=100, default='null')
    lng = models.CharField(max_length=100, default='null')
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
    payrate = models.CharField(max_length=10, default=0)
    billrate = models.CharField(max_length=10, default=0)
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

class Worker(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=CASCADE
    )
    shifts = models.ManyToManyField(
        Shift,
        related_name='claimed_shifts'
    )
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
