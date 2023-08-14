import telnetlib
import socket
import time
import datetime
import os
from concurrent.futures import ThreadPoolExecutor
from itertools import repeat

def to_bytes(line):
    return f"{line}\n".encode("utf-8")


def connect_and_set_command(device, command, timeout=20):
    ip = device["host"]
    try:
        with telnetlib.Telnet(ip, timeout=timeout) as telnet:
            login = ""
            telnet.read_until(b'UserName:', timeout=5)
            telnet.write(b'username\n')
            telnet.write(b'password\n')
            login += str(telnet.read_until(b'#', timeout=5))
            login += str(telnet.read_until(b'user#', timeout=5))
            if "user#" in login:
                telnet.write(b'enable admin\n')
                telnet.write(b'password\n')
            telnet.write(b'\n')
            telnet.write(to_bytes(command))
            telnet.write(b'a')
            time.sleep(40)
            result = telnet.read_very_eager().decode('ascii')
            telnet.close()
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

    device = []

    with open("ip.txt") as file:
        for ip in file:
            dev_ip = ip.rstrip()
            device.append({"host": dev_ip})


    with ThreadPoolExecutor(max_workers=10) as executor:
        result = executor.map(connect_and_set_command, device, repeat('enable authen_policy\n'))
        print(result)
        date_1 = datetime.datetime.now()
        date = str(date_1).split()[0]
        for dev, output in zip(device, result):
            print(dev, output)
            with open(f'logs/{folder}/{dev["host"]}-{date}.txt', 'w', encoding='UTF-8') as f:
                f.writelines(f"{output}")
