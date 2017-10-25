from __future__ import unicode_literals
from django.db import models
from ..users.models import User, Host
from datetime import date, datetime
# Create your models here.

class Place(models.Model):
    name = models.CharField(max_length=255)
    host = models.ForeignKey(Host,related_name="places")
    place_type = models.CharField(max_length=255)
    shared = models.CharField(max_length=255)
    rooms = models.IntegerField(blank=False)
    guests = models.IntegerField(blank=False)
    beds = models.IntegerField(blank=False)
    baths = models.IntegerField(blank=False)
    private_bath = models.BooleanField(default=False)
    country = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    apt_number = models.IntegerField(blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip = models.IntegerField(blank=False)
    price = models.IntegerField(blank=False)
    desc = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    
class Amenity(models.Model):
    name = models.CharField(max_length=255)
    place = models.ForeignKey(Place, related_name="amenities")

class Trip(models.Model):
    place = models.ForeignKey(Place, related_name="place_trips")
    user = models.ForeignKey(User, related_name="user_trips")
    guests = models.IntegerField(blank=False)
    start_date = models.DateTimeField(default=datetime.now, blank=True)
    end_date = models.DateTimeField(default=datetime.now, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Place_Review(models.Model):
    content = models.CharField(max_length=255)
    rating = models.IntegerField(blank=False)
    place = models.ForeignKey(Place,related_name="reviews")
    rated_by = models.ForeignKey(User,related_name="place_reviews")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)