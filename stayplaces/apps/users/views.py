from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from django.utils.crypto import get_random_string
from models import User, Host, Host_Review
from ..locations.models import Place, Amenity, Trip, Place_Review
import bcrypt
import re
from datetime import datetime, date
from django.utils import timezone

#------------------------ Page Loading --------------------------#


# Load home page
def index(request):
    places = Place.objects.all()
    if 'id' in request.session:
        #Get Logged in User
        user = User.objects.get(id = request.session['id'])
        
        #Check if logged in user is host
        if hasattr(user, 'host'):
            host = True
        else:
            host = False
        
        context = {
            'User': user,
            'Places': places,
            'Host': host,
        }
        return render(request , "users/index.html", context)

    else:
        return render(request , "users/index.html")

def listing(request, id):
    user = User.objects.get(id=id)
    if request.method == "POST":
        name = request.POST['name']
        place_type = request.POST['place_type']
        shared = request.POST['shared']
        rooms = request.POST['rooms']
        guests = request.POST['guests']
        beds = request.POST['beds']
        baths = request.POST['baths']
        private_bath = request.POST['private_bath']
        country = request.POST['country']
        street_address = request.POST['street_address']
        apt_number = request.POST['apt_number']
        city = request.POST['city']
        state = request.POST['state']
        zip = request.POST['zip']
        price = request.POST['price']
        amenities = request.POST.getlist('amenities')


        if private_bath == "Yes":
            private_bath = True
        else:
            private_bath = False

        if len(Host.objects.filter(user = user)) == 0:
            Host.objects.create(user = user)
            host = Host.objects.get(user = user)
        else:
            host = Host.objects.get(user = user)

        Place.objects.create(name=name, host=host, place_type=place_type, shared=shared, rooms=rooms, guests=guests,beds=beds, baths=baths, private_bath=private_bath, country=country, street_address=street_address, apt_number=apt_number, city=city, zip=zip, price=price)
        
        current_place = Place.objects.get(street_address = street_address)
        for a in amenities:
            Amenity.objects.create(name = a, place = current_place)

        return redirect("/")
            
    else:
        user = User.objects.get(id = request.session['id'])
        host = user.host
        #Check if logged in user is host
        if hasattr(user, 'host'):
            host_log = True
        else:
            host_log = False
        context = {
            'places': host.places.all(),
            'User': user,
            'Host': host_log
        }
        return render(request , 'users/listings.html', context)

def trips(request):
    user = User.objects.get(id = request.session['id'])
    today = datetime.utcnow()
    now = timezone.now()
    trips = Trip.objects.filter(user = user)

    #Keep Track if trip is coming up or in the past
    upcoming = []
    past = []
    for trip in trips:
        if trip.end_date >= now:
            upcoming.append(trip)
        else:
            past.append(trip)

    #Check if logged in user is host
    if hasattr(user, 'host'):
        host_log = True
    else:
        host_log = False

    context = {
        'User': user,
        'Host': host_log,
        'upcoming': upcoming,
        'past':past
    }
    return render(request , 'users/trips.html', context)

def review(request, id):
    user = User.objects.get(id = request.session['id'])
    trip = Trip.objects.get(id = id)
    place = trip.place
    host = trip.place.host
    try:
        review = user.host_reviews.get(host = host)
    except:
        review = None
    try:
        place_review = user.place_reviews.get(place = place)
    except:
        place_review = None
    print review
    #Check if logged in user is host
    if hasattr(user, 'host'):
        host_log = True
    else:
        host_log = False

    context = {
        'User': user,
        'Host': host_log,
        'host_review': host,
        'place': place,
        'review': review,
        'place_review': place_review
    }

    return render(request , 'users/reviews.html', context)

def host_review(request, id):
    rating = request.POST['rating']
    content = request.POST['message']
    user_id = request.POST['rated_by']
    user = User.objects.get(id = user_id)
    host = Host.objects.get(id=id)
    Host_Review.objects.create(rating=rating, content=content, rated_by=user, host=host )
    return redirect('/trips')

def place_review(request, id):
    rating = request.POST['rating']
    content = request.POST['message']
    user_id = request.POST['rated_by']
    user = User.objects.get(id = user_id)
    place = Place.objects.get(id=id)
    Place_Review.objects.create(rating=rating, content=content, rated_by=user, place=place )
    return redirect('/trips')

def hosting(request): 
    if 'id' in request.session:
        user = User.objects.get(id = request.session['id'])

        #Check if logged in user is host
        if hasattr(user, 'host'):
            host_log = True
        else:
            host_log = False
        context = {
            'User': user,
            'Host': host_log 
        }
        return render(request , "users/host.html", context)
    else:
        return render(request , "users/host.html")

def profile(request, id): 
    if 'id' in request.session:
        user = User.objects.get(id = request.session['id'])
        profile = User.objects.get(id = id)
        try:
            places = Place.objects.filter(host = profile.host)
            reviews = Host_Review.objects.filter(host = profile.host)
        except:
            places = None
            reviews = None
        print places
        #Check if logged in user is host
        if hasattr(user, 'host'):
            host_log = True
        else:
            host_log = False

        #Check if profile user is host
        if hasattr(profile, 'host'):
            profile_host = True
        else:
            profile_host = False

        context = {
            'User': user,
            'Host': host_log,
            'Profile': profile,
            'Profile_host': profile_host ,
            'Places': places,
            'reviews': reviews
        }
        return render(request , "users/profile.html", context)
    else:
        return render(request , "users/profile.html")

def edit_profile(request): 
    if 'id' in request.session:
        user = User.objects.get(id = request.session['id'])
        #Check if logged in user is host
        if hasattr(user, 'host'):
            host_log = True
        else:
            host_log = False

        context = {
            'User': user,
            'Host': host_log,
        }
        return render(request , "users/edit.html", context)
    else:
        return render(request , "users/edit.html")

def upload(request):
    user = User.objects.get(id = request.session['id'])
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        user.photo = myfile
        user.save
        return redirect('/')    

def edit(request, id):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    gender = request.POST['gender']
    email = request.POST['email']
    phone = request.POST['phone']
    location = request.POST['location']
    desc = request.POST['desc']
    


#------------------------ LOGIN CODE --------------------------#

def register(request):
    if request.method == "POST":
        #Validation in models.py AND creates user if no errors
        valid, response = User.objects.register_validator(request.POST)
        if valid:
            request.session['id'] = response.id
            return redirect('/')
        else:
            for message in response:
                messages.error(request, message)
            return redirect('/login')
    else:
        return redirect('/')

def login(request):
    if request.method == "POST":
        #Validation in models.py
        valid, response = User.objects.login_validator(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        if valid:
            request.session['id'] = response.id
            return redirect("/")
        else:
            for message in response:
                messages.error(request, message)
            return redirect('/login')
    else:
        context = {
        'Users': User.objects.all(),
    }
    return render(request , "users/login.html", context)
         
def logout(request):
    del request.session['id']
    return redirect("/")
