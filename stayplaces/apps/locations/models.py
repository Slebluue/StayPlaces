from __future__ import unicode_literals
from django.db import models
from ..users.models import User, Host
from datetime import date, datetime
import googlemaps
from jsonfield import JSONField
gmaps = googlemaps.Client(key='AIzaSyCjQRMAgIaJyoNrUyhDCT5c470E6AkvDik')

# Create your models here.
class LocationManager(models.Manager):
    #REGISTER VALIDATION
    def loaction_register_validator(self, postData, fileData, user):
        errors = []

        #Post data variables
        name = postData['name']
        desc = postData['desc']
        place_type = postData['place_type']
        shared = postData['shared']
        rooms = postData['rooms']
        guests = postData['guests']
        beds = postData['beds']
        baths = postData['baths']
        private_bath = postData['private_bath']
        country = postData['country']
        street_address = postData['street_address']
        city = postData['city']
        state = postData['state']
        zip = postData['zip']
        price = postData['price']
        amenities = postData.getlist('amenities')

        #Basic validations for register
        if len(name) < 1 or len(desc) < 1 or len(price) < 1 or len(street_address) < 1 or len(city) < 1 or len(zip) < 1:
            errors.append('Please fill out all fields')
        if len(zip) > 5:
            errors.append('Please enter valid zipcode')

        try:
            geocode = gmaps.geocode(street_address+', '+city+', '+state)
            geocode = geocode[0]
            # print geocode
            lat = geocode['geometry']['location']['lat']
            lng = geocode['geometry']['location']['lng']
        except:
            print "Not a valid address"
            errors.append('Please enter a valid address')

        try:
            image = fileData['image']
        except:
            image = None

        if len(errors):
            return (False, errors)
        else:
            #Success set hashed pw and create new user
            if len(Host.objects.filter(user = user)) == 0:
                Host.objects.create(user = user)
                host = Host.objects.get(user = user)
            else:
                host = Host.objects.get(user = user)

            self.create(name=name, host=host, place_type=place_type, shared=shared, rooms=rooms, guests=guests,beds=beds, baths=baths, private_bath=private_bath, country=country, street_address=street_address, city=city, zip=zip, price=price, image=image, geocode=geocode, long_position = lng, lat_position = lat)
            current_place = self.get(street_address = street_address)
            for a in amenities:
                Amenity.objects.create(name = a, place = current_place)
            return (True, current_place)


class Place(models.Model):
    name = models.CharField(max_length=255)
    host = models.ForeignKey(Host,related_name="places")
    place_type = models.CharField(max_length=255)
    shared = models.CharField(max_length=255)
    rooms = models.IntegerField(blank=False)
    guests = models.IntegerField(blank=False)
    beds = models.IntegerField(blank=False)
    baths = models.IntegerField(blank=False)
    private_bath = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    zip = models.IntegerField(blank=False)
    price = models.IntegerField(blank=False)
    desc = models.CharField(max_length=255, null=True, blank=True)
    image = models.FileField(upload_to='media/%Y/%m/%d',null=True, blank=True)
    geocode = JSONField(null=True, blank=True)
    long_position = models.DecimalField (max_digits=11, decimal_places=7, null=True, blank=True)
    lat_position = models.DecimalField (max_digits=11, decimal_places=7, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    #Add UserManager functionality to user.objects
    objects = LocationManager()
    
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