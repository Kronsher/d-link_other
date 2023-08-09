import netmiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)
import datetime
import os

def connect_to_device(ip):
    device = {
        "device_type": "dlink_ds",
        'ip':   f'{ip}',
        'username': 'admin',
        'password': 'Intr1X'

    }
    try:
        ssh = netmiko.ConnectHandler(**device)

        output = ssh.send_command('show config current_config')
        return output
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as error:
        print(error)

def make_folder():
    date_1 = datetime.datetime.now()
    date2 = str(date_1).split()[0]
    date = date2[:7]
    if not os.path.isdir(f"logs/{date}/"):
        os.mkdir(f"logs/{date}")
    return date

folder = make_folder()

print(folder)

if __name__ == "__main__":
    make_folder()
    date_1 = datetime.datetime.now()
    date = date = str(date_1).split()[0]
    with open("ip.txt", "r") as file:
        for ip in file:
            print(ip)
            result = connect_to_device(ip)
            date_1 = datetime.datetime.now()
            date = date = str(date_1).split()[0]
            dev_ip = ip.rstrip()
            with open(f'logs/{folder}/{dev_ip}-{date}.txt', 'w', encoding='UTF-8') as f:
                f.writelines(f"{result}")