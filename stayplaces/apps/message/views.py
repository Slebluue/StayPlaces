from django.contrib import messages
from django.shortcuts import render, HttpResponse, redirect
from django.utils.crypto import get_random_string
from django.db.models import Avg, Max
from ..users.models import User, Host
from ..locations.models import Place, Amenity
from models import Message, Conversation
import bcrypt
import re

#------------------------ Page Loading --------------------------#


# Load home page
def index(request):
    if 'id' in request.session:
        #Get Logged in User
        user = User.objects.get(id = request.session['id'])
    
        # get the conversations the user is in
        host_conversation_list = Conversation.objects.filter(host=user)
        guest_conversation_list = Conversation.objects.filter(guest=user)
        #Check if logged in user is host
        if hasattr(user, 'host'):
            host = True
        else:
            host = False
        
        context = {
            'User': user,
            'Host': host,
            'conversation_list': host_conversation_list,
            'guest_list': guest_conversation_list
        }
        return render(request , "messages/inbox.html", context)

    else:
        return render(request , "users/index.html")

def host_conversation(request, id):
    if request.method ==  "POST":
        conversation = Conversation.objects.get(id = id)
        user = User.objects.get(id = request.session['id'])
        host = conversation.host
        guest = conversation.guest
        content = request.POST['message']

        if len(Conversation.objects.filter(host = host, guest = guest )) > 0:
            conversation = Conversation.objects.get(host = host, guest = guest)
            conversation.messages.add(Message.objects.create(content = content, host = host, guest = guest, sender_id=user.id,  conversation = conversation))
            conversation.save()
        
        else:
            conversation = Conversation.objects.create(host = host, guest = guest)
            Message.objects.create(content = content, host = host, guest = guest, conversation=conversation)
        
        
        return redirect("/inbox/host-conversation/"+id)
    else:
        if 'id' in request.session:
            #Get Logged in User
            user = User.objects.get(id = request.session['id'])
            
            # get the specific Guest user conversation
            conversation = Conversation.objects.get(id= id)
            guest = conversation.guest
            context = {
                'User': user,
                'conversation': conversation.messages.all(),
                'Host': conversation.host,
                'Guest': guest,
                'conversation_id': id
            }
            return render(request , "messages/host-conversation.html", context)

        else:
            return redirect('/')

def user_conversation(request, id):
    if request.method ==  "POST":
        user = User.objects.get(id = request.session['id'])
        conversation = Conversation.objects.get(id = id)
        host = conversation.host
        guest = conversation.guest
        content = request.POST['message']

        if len(Conversation.objects.filter(host = host, guest = guest )) > 0:
            conversation = Conversation.objects.get(host = host, guest = guest)
            conversation.messages.add(Message.objects.create(content = content, host = host, guest = guest, sender_id=user.id,  conversation = conversation))
            conversation.save()
        
        else:
            conversation = Conversation.objects.create(host = host, guest = guest)
            Message.objects.create(content = content, host = host, guest = guest, conversation=conversation)
        
        
        return redirect("/inbox/user-conversation/"+id)
    else:
        if 'id' in request.session:
            #Get Logged in User
            user = User.objects.get(id = request.session['id'])
        
            # get the conversation
            conversation = Conversation.objects.get(id= id)
            guest = conversation.guest

            context = {
                'User': user,
                'Guest': guest,
                'conversation': conversation.messages.all(),
                'Host': conversation.host,
                'conversation_id': id
            }
            return render(request , "messages/user-conversation.html", context)

        else:
            return redirect('/')

def send(request, id):
    host = User.objects.get(id = id)
    guest = User.objects.get(id = request.session['id'])
    content = request.POST['message']

    if len(Conversation.objects.filter(host = host, guest = guest )) > 0:
        conversation = Conversation.objects.get(host = host, guest = guest)
        conversation.messages.add(Message.objects.create(content = content, host = host, guest = guest, sender_id=guest.id,  conversation = conversation))
        conversation.save()
    
    else:
        conversation = Conversation.objects.create(host = host, guest = guest)
        Message.objects.create(content = content, host = host, guest = guest, sender_id=guest.id, conversation=conversation)
    
    
    return redirect("/users/show/"+id)
