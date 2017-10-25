from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from django.utils.crypto import get_random_string
from .. users.models import User
from models import Place, Trip
import bcrypt
import re
from datetime import datetime
#------------------------ LOGIN CODE --------------------------#
# Load home page
def index(request):
    if 'id' in request.session:
        user = User.objects.get(id = request.session['id'])
        places = Place.objects.all()
        
        context = {
            'User': user, 
            'places': places,
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
        context = {
            'User': user, 
            'place': place,
            'amenities': amenities,
            'guests': guests,
            'reviews': reviews
        }
        return render(request , "locations/show.html", context)

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