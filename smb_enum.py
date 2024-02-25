from impacket.smbconnection import SMBConnection
from termcolor import colored
import sys

def anonLoginSMB(hostname):
    try:
        conn = SMBConnection(hostname, hostname, timeout=5)
        conn.login('', '')  # Empty username and password for anonymous login
        print(colored(f"[*] {hostname} SMB Guest Logon Succeeded", 'green'))
        conn.close()
        return True
    except Exception as e:
        print(colored(f"[-] {hostname} SMB Guest Logon Failed: {e}", 'red'))
        return False

# Example usage:
# anonLoginSMB('hostname_or_ip_address')

if len(sys.argv) != 2:
    print("Usage: smb_enum.py <host>")
else:
    anonLoginSMB('192.168.58.136')
