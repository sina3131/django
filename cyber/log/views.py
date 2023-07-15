from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from cybersec.decorators import unauthenticated_user, allowed_users, is_superuser
from cybersec.forms import *
from django.contrib.auth.models import Group
from gvm.connections import UnixSocketConnection
from gvm.protocols.latest import Gmp
import nmap


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


@login_required
def scaning(request):
    if request.method == "POST":
        form_1 = Deive_form(request.POST)
        if form_1.is_valid():
            user = form_1.save()
            data = form_1.cleaned_data
            device_name = data.get('device_name')
            ip_address = data.get('ip_address')
            port = data.get('port_info')
            print(f"Scanning device: {device_name}")
            print(f"IP address: {ip_address}")
            target = PortScanner(ip_address, port)
            target.scan()

            with open(vul_file, 'r') as file:
                count = 0
                for banner in target.banners:
                    file.seek(0)
                    for line in file.readlines():
                        if line.strip() in banner:
                            resultss = '[!!] VULNERABLE BANNER: "' + banner + '" ON PORT: ' + str(target.open_ports[count])
                    count += 1
            messages.success(request, "Scan completed successfully.")
            return redirect('/log/scan_result')  # Redirect back to the scan page after successful scan
    else:
        form_1 = Deive_form()
    context = {'form_1': form_1}
    return render(request, "scan.html", context)

def store_scan_result():
    



# def nmap_scan(target_ip):
#     nm = nmap.PortScanner()
#     nm.scan(target_ip, arguments='Pn -sV -O')
#     vluneberities = process(nm)
#     return vluneberities


# def process(nmap_result):
#     vluner = []
#     for h in nmap_result.all_hosts():
#         if 'tcp' in nmap_result[h]:
#             for port in nmap_result[h]['tcp']:
#                 if 'vuln' in nmap_result[h]['tcp'][port]:
#                     for vl in nmap_result[h]['tcp'][port]['vlun']:
#                         vluner.append({
#                             'ip_address': h,
#                             'port': port,
#                             'vuleberity': vluner,
#                         })
#     return vluner

def scan_result(request):
    device_info = Device.objects.all()
    user_info = User.objects.all()
    return render( request, "scan_result.html", {'device_info': device_info, 'user_info': user_info})





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


import socket
from IPy import IP


class PortScanner:
    banners = ['Vulnerable Software XYZ']
    open_ports = [500, 501]

    def __init__(self, target, port_num):
        self.target = target
        self.port_num = port_num

    def scan(self):
        for port in range(1, self.port_num + 1):
            self.scan_port(port)

    def check_ip(self):
        try:
            IP(self.target)
            return self.target
        except ValueError:
            return socket.gethostbyname(self.target)

    def scan_port(self, port):
        try:
            converted_ip = self.check_ip()
            sock = socket.socket()
            sock.settimeout(0.5)
            sock.connect((converted_ip, port))
            self.open_ports.append(port)
            try:
                banner = sock.recv(1024).decode().strip('\n').strip('\r')
                self.banners.append(banner)
            except:
                self.banners.append('')
            sock.close()
        except:
            pass

targets_ip = input('[+] * Enter Target To Scan For Vulnerable Open Ports: ')
port_number = int(input('[+] * Enter Amount Of Ports You Want To Scan (500 - First 500 Ports): '))
vul_file = input('[+] * Enter Path To The File With Vulnerable Softwares: ')
print('\n')

target = PortScanner(targets_ip, port_number)
target.scan()

with open(vul_file, 'r') as file:
    count = 0
    for banner in target.banners:
        file.seek(0)
        for line in file.readlines():
            if line.strip() in banner:
                print('[!!] VULNERABLE BANNER: "' + banner + '" ON PORT: ' + str(target.open_ports[count]))
        count += 1