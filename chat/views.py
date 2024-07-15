from django.http import HttpResponseNotAllowed, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .forms import RegisterForm
from .models import Chat, Message
import json


# request: Objekt, wird standardmäßig in diese Funktion reingegeben
@login_required(login_url='/login/')
def index(request):
    if request.method == 'POST':
        text_message = request.POST.get('textmessage')
        if text_message:
            myChat = Chat.objects.get(id=1)
            new_message = Message.objects.create(
                text=text_message,
                chat=myChat,
                author=request.user,
                receiver=request.user
            )
            serialized_obj = serializers.serialize('json', [new_message])       # Serialize the new message object and return it as JSON
            return JsonResponse(serialized_obj[1:-1], safe=False)
        else:
            return JsonResponse({'error': 'No text message provided'}, status=400)
    
    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, 'chat/index.html', {'messages': chatMessages})

# Message.objects.create: Können auf unsere Datenbank zugreifen, create: Neue Instanz in Datenbank erstellen

@csrf_exempt
@login_required(login_url='/login/')
def delete_message(request, message_id):
    if request.method == 'DELETE':
        try:
            message = Message.objects.get(id=message_id, author=request.user)
            message.delete()
            return JsonResponse({'success': True})
        except Message.DoesNotExist:
            return JsonResponse({'error': 'Message not found or not authorized'}, status=404)
    return HttpResponseNotAllowed(['DELETE'])


def login_view(request):
	login_in_progress = False
	redirect_to = request.POST.get('redirect', request.GET.get('next', ''))
	print(f"Redirect parameter: {redirect}") 
	if request.method == 'POST':
		user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
		login_in_progress = True 
		if user:
			login(request, user)
			return HttpResponseRedirect(redirect_to)
		else:
			return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': redirect_to, 'login_in_progress': login_in_progress})
	login_in_progress = False	
	return render(request, 'auth/login.html', {'redirect': redirect_to})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')  # Verwende hier den Namen der Login-View
    return render(request, 'auth/logout.html') 


def register_view(response):
	if response.method == "POST":
		form = RegisterForm(response.POST)
		if form.is_valid():
			form.save()
			return redirect("/chat")
		else:
			print(form.errors)  
			messages.error(response, 'There was an error in your registration form.')
	else:
		form = RegisterForm()

	return render(response, "register/register.html", {"form": form})


# def delete_view(request, id):
#     context ={}
 
#     # fetch the object related to passed id
#     obj = get_object_or_404(Message, id = id)
 
 
#     if request.method =="POST":
#         # delete object
#         obj.delete()
#         # after deleting redirect to 
#         # home page
#         return HttpResponseRedirect("/")
 
#     return render(request, "delete_view.html", context)

