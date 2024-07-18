from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
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


# @login_required(login_url='/login/')
@csrf_exempt
@require_http_methods(["PATCH"])
def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.user != message.author:
        return HttpResponse(status=403)

    try:
        data = json.loads(request.body)
        message.text = data['text']  # 'text' ist der Name des Feldes, das du aktualisieren möchtest
        message.save()
        return JsonResponse({'status': 'success', 'message': message.text})
    except (KeyError, ValueError):
        return JsonResponse({'status': 'error', 'message': 'Invalid data'}, status=400)
                  


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

	return render(response, "auth/register.html", {"form": form})
