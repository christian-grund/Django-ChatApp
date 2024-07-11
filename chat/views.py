from django.http import HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import Chat, Message
from django.http import HttpResponse
from django.template import loader


# request: Objekt, wird standardmäßig in diese Funktion reingegeben
@login_required(login_url='/login/')
def index(request):
	if request.method == 'POST':
		print("Received data: " + request.POST['textmessage'])
		myChat = Chat.objects.get(id=1)
		new_message = Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user)  # Nachricht wird erstellt
		serialized_obj = serializers.serialize('json', [ new_message, ])
		return JsonResponse(serialized_obj[1:-1], safe=False)
	chatMessages = Message.objects.filter(chat__id=1)                            
	return render(request, 'chat/index.html', {'messages': chatMessages})

# Message.objects.create: Können auf unsere Datenbank zugreifen, create: Neue Instanz in Datenbank erstellen


def login_view(request):
	redirect = request.GET.get('next')
	print(f"Redirect parameter: {redirect}") 
	if request.method == 'POST':
		user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
		if user:
			login(request, user)
			return HttpResponseRedirect(request.POST.get('redirect'))
		else:
			return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': redirect})
	return render(request, 'auth/login.html', {'redirect': redirect})


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

def test_static(request):
    template = loader.get_template('base.html')
    return HttpResponse(template.render({}, request))


