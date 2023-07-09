from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from cybersec.decorators import unauthenticated_user, allowed_users, is_superuser
from cybersec.forms import *
from django.contrib.auth.models import Group


def registerPage(request):
    form = createUserForm()
    if request.method == "POST":
        form = createUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            data = form.cleaned_data
            messages.success(request, f"Account created for {data['first_name']} {data['last_name']}")
            message = f"""Welcome {data['first_name']} {data['last_name']} to us"""
            group, created = Group.objects.get_or_create(name='customer')
            user.groups.add(group)
            # send_mail('New cyber Account', message, 'settings.EMAIL_HOST_USER', [data["email"]], fail_silently=False)
            return redirect("login")
    error_messages = [error[0] for error in form.errors.values()]
    content = {'form': form, 'errors':error_messages}
    return render(request, "registration/register.html", content)

# @login_required
# def scan (request):
#     form_1 = Deive_form()
#     if request.method == "POST":
#         form_1 = Deive_form(request.POST)
#         if form_1.is_valid():
#             user = form_1.save()
#             data = form_1.cleaned_data
#             messages.success(request, f"Your device name is {data['device_name']} Your ip address is {data['ip_address']}")
#             message = f"""the scan will be applied to {data['device_name']} {data['ip_address']} """
#             # group, created = Group.objects.get_or_create(name='customer')
#             # user.groups.add(group)
#             # send_mail('New cyber Account', message, 'settings.EMAIL_HOST_USER', [data["email"]], fail_silently=False)
#             # return redirect("login")
#     error_messages = [error[0] for error in form_1.errors.values()]
#     content = {'form_1': form_1, 'errors':error_messages}
#     return render(request, "scan_result.html", content)

@login_required
def scaning(request):
    if request.method == "POST":
        form_1 = Deive_form(request.POST)
        if form_1.is_valid():
            data = form_1.cleaned_data
            device_name = data.get('device_name')
            ip_address = data.get('ip_address')
            print(f"Scanning device: {device_name}")
            print(f"IP address: {ip_address}")

            # Perform your scanning logic here
            # You can replace the print statements with your actual scanning code

            messages.success(request, "Scan completed successfully.")
            return redirect('/log/scan_result')  # Redirect back to the scan page after successful scan

    else:
        form_1 = Deive_form()

    context = {'form_1': form_1}
    return render(request, "scan.html", context)

def scan_result(request):
    return render( request, "scan_result.html")






def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request , "there was an error")
            return redirect('login')
    else:
        return render(request, 'registration/login.html')
    
@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            if user.last_login is None:
                login(request, user)
                return redirect('edit_profil')
            else:
                login(request, user)
                next = request.GET.get('next')
                if next:
                    return redirect(next, 'index')
                else:
                    return redirect('index')
        else:

            messages.error(request, 'Username or password incorrect')

    return render(request, "login.html")

def logout_user(request):
    logout(request)
    messages.success(request, ("You were logged out"))
    return redirect('home')
        