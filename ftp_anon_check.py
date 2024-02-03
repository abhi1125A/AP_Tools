#!/usr/bin/python3
import ftplib
import sys
from termcolor import colored
from threading import *
import optparse

def anonLogin(hostname):
    try:
        ftp=ftplib.FTP(hostname)
        ftp.login('anonymous', 'anonymous')
        print(colored(f"[*] {hostname} FTP Anonymous Logon Succeeded", 'green'))
        ftp.quit()
        return True
    except:
        print(colored(f"[-] {hostname} FTP Anonymous Logon failed", 'red'))

num_args = len(sys.argv) - 1

parser = optparse.OptionParser('Usage of Program: ' + './ftp_anon_check.py -H [target]')
parser.add_option('-H', dest='tgtHost', type='string', help='specify the target host')

(options, args) = parser.parse_args()
tgtHost=options.tgtHost

if (tgtHost == None):
    print(parser.usage)
    exit(0)
anonLogin(tgtHost)
