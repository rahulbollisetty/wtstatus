from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate,logout 
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
import requests
def index(request):
    data = True
    result = None
    globalSummary = None
    countries = None
    while(data):
        try:
            result = requests.get('https://api.covid19api.com/summary')
            json = result.json()

            globalSummary = json['Global']
            countries = json['Countries']

            data = False
        except:
            data = True
    return render(request , 'index.html' ,
                  {'globalSummary' : globalSummary ,
                   'countries' : countries})
def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            messages.success(request,"Registration successful.")
            return redirect('index')
        messages.error(request,"Unsuccessful registration.Invalid Information")
    form =NewUserForm
    return render(request,'register.html',context={"register_form":form})
def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("index")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("index")