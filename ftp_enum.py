#!/usr/bin/python3

from socket import *
import optparse
from threading import Thread
import ftplib
from termcolor import colored
from impacket.smbconnection import SMBConnection

port_list = [] 

def connScan(tgtHost, tgtPort):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.settimeout(1)
    try:
        sock.connect((tgtHost, tgtPort))
        global port_list
        port_list.append(tgtPort)
        print(colored(f"[+]    {tgtPort}/tcp     open", 'green'))
    except:
        pass
    finally:
        sock.close()

def Enumeration(tgtHost):
    print(colored('========== Enumeration Phase ==========', 'green'))
    for port in port_list:
        if port == 21:
            try:
                ftp=ftplib.FTP(tgtHost)
                ftp.login('anonymous','anonymous')
                print("FTP Enumeration")
                print(colored(f"\t [*] {tgtHost} FTP Anonymous Logon Succeeded", 'green'))
                ftp.quit()
            except:
                pass
        if port == 445:
            try:
                conn = SMBConnection(tgtHost, tgtHost, timeout=5)
                conn.login('', '')  # Empty username and password for anonymous login
                print("SMB Enumertion")
                print(colored(f"\t [*] {tgtHost} SMB Guest Logon Succeeded", 'green'))
                conn.close()
                return True
            except Exception as e:
                print(e)

    return

def sRange(tgtHost, tgtSRange):
    start, end = map(int, tgtSRange.split('-'))
    for tgtPort in range(start, end + 1):
        t = Thread(target=connScan, args=(tgtHost, tgtPort))
        t.start()

def portScan(tgtHost, tgtPorts):
    for tgtPort in tgtPorts.split(','):
        t = Thread(target=connScan, args=(tgtHost, int(tgtPort)))
        t.start()
        t.join()

def rangeScan(tgtHost, tgtRange):
    for tgtPort in range(int(tgtRange) + 1):
        t = Thread(target=connScan, args=(tgtHost, tgtPort))
        t.start()

def main():
    parser = optparse.OptionParser('Usage of Program: ' + './portscan.py -H [target] -p [port] OR -r [range] OR -s [specific range]' + """
    Example:
    ./portscan.py -H 192.168.25.10 -p 21,22,23,25,88
    ./portscan.py -H 192.168.25.10 -r 100
    ./portscan.py -H 192.168.25.10 -s 3000-4000""")
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
    parser.add_option('-p', dest='tgtPort', type='string', help='specify the target port(s) separated by commas')
    parser.add_option('-r', dest='tgtRange', type='string', help='specify the target range of port')
    parser.add_option('-s', dest='tgtSRange', type='string', help='specify the specific range of ports to scan')
    (options, args) = parser.parse_args()
    tgtHost = options.tgtHost
    tgtPorts = options.tgtPort
    tgtRange = options.tgtRange
    tgtSRange=options.tgtSRange
    if tgtHost is None or (tgtPorts is None and tgtRange is None and tgtSRange is None):
        print(parser.usage)
        exit(0)
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        print("Can't resolve the target host")
        return

    try:
        tgtName = gethostbyaddr(tgtIP)
        print(f"Scan results for: {tgtName[0]}")
    except:
        print(f"Scan results for: {tgtIP}")
    if tgtRange is None and tgtSRange is None:
        portScan(tgtHost, tgtPorts)
        Enumeration(tgtHost)
    elif tgtPorts is None and tgtSRange is None:
        rangeScan(tgtHost, tgtRange)
        Enumeration(tgtHost)
    else:
        sRange(tgtHost, tgtSRange)
        Enumeration(tgtHost)

if __name__ == '__main__':
    main()

