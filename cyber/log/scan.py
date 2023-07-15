

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