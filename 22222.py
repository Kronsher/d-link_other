import socket
import datetime
import os
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat
from netmiko import ConnectHandler


def to_bytes(line):
    return f"{line}\n".encode("utf-8")



def connect_and_set_command(ip, command):
    dlink_device = {
        'device_type': 'dlink_ds',
        'ip': '172.16.111.2',
        'username': 'admin',
        'password': 'Intr1X',
        'port': 22,
        'verbose': 'True',
        'session_timeout': 60,
    }
    try:
        with ConnectHandler(**dlink_device) as ssh:
            output = ssh.send_command(command, read_timeout=60)
            print(output)
            return result
    except socket.timeout:
        print("Timeout")
    except UnicodeDecodeError:
        print("Error code")

def make_folder():
    date_1 = datetime.datetime.now()
    date2 = str(date_1).split()[0]
    date = date2[:7]
    if not os.path.isdir(f"logs/{date}/"):
        os.mkdir(f"logs/{date}")
    return date

folder = make_folder()
#
if __name__ == "__main__":
    make_folder()


    with open("ip.txt") as file:
        for ip in file:
            dev_ip = ip.rstrip()



    with ThreadPoolExecutor(max_workers=10) as executor:
        result = executor.map(connect_and_set_command, dev_ip, repeat("show config current_config\n"))
        print(result)
        date_1 = datetime.datetime.now()
        date = str(date_1).split()[0]
        for dev, output in zip(dev_ip, result):
            print(dev, output)
            with open(f'logs/{folder}/{dev["host"]}-{date}.txt', 'w', encoding='UTF-8') as f:
                f.writelines(f"{output}")