from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm
from django.contrib import messages

def carlist(request):
    return render(request, "accounts/carlist.html")

def customer(request):
    return render(request,"accounts/customer.html")

def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            messages.success(response, "Your account has been created successfully! You can now login")
            return redirect("/login")
        else:
            messages.error(response, "There was an error in the form. Please try again.")
    else:
        form = RegisterForm()

    return render(response, "accounts/register.html", {"form":form})


from django.shortcuts import render

def start_view(request):
    return render(request, 'accounts/start.html')

def contact_view(request):
    return render(request, 'accounts/contact.html')


