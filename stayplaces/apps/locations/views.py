from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from django.utils.crypto import get_random_string
from .. users.models import User
from models import Place, Trip
import bcrypt
import re
from datetime import datetime
import googlemaps
gmaps = googlemaps.Client(key='AIzaSyCjQRMAgIaJyoNrUyhDCT5c470E6AkvDik')

#------------------------ LOGIN CODE --------------------------#
# Load home page
def index(request):
    if 'id' in request.session:
        user = User.objects.get(id = request.session['id'])
        places = Place.objects.all()
        search = request.session['geocode']
        filtered = []
        for place in places:
            if place.city in search:
                filtered.append(place)

        context = {
            'User': user, 
            'places': filtered,
        }
        return render(request , "locations/index.html", context)
    else:
        return render(request , "locations/index.html")

def show(request, id):
    if 'id' in request.session:
        user = User.objects.get(id = request.session['id'])
        place = Place.objects.get(id = id)
        amenities = place.amenities.all()
        reviews = place.reviews.all()
        guests = range(place.guests)

        if hasattr(user, 'host'):
            host = True
        else:
            host = False
        
        context = {
            'User': user, 
            'place': place,
            'amenities': amenities,
            'guests': guests,
            'reviews': reviews,
            'Host': host
        }
        return render(request , "locations/show.html", context)
    else:
        user = None
        place = Place.objects.get(id = id)
        amenities = place.amenities.all()
        reviews = place.reviews.all()
        guests = range(place.guests)
        context = {
            'User': user,
            'place': place,
            'amenities': amenities,
            'guests': guests,
            'reviews': reviews
        }
        return render(request , "locations/show.html", context)

def search(request):
    search = request.POST['search']
    print search
    geocode = gmaps.geocode(search)
    request.session['geocode'] = search
    return redirect('/s')

    

def book(request,id):
    user = User.objects.get(id = request.session['id'])
    place = Place.objects.get(id = id)
    start_date = request.POST['startdate']
    end_date = request.POST['enddate']
    guests = request.POST['guests']
    Trip.objects.create(place = place, user=user, guests=guests, start_date=start_date, end_date=end_date)
    print start_date
    print end_date
    print guests
    return redirect ("/s/rooms/"+id)