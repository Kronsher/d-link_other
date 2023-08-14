import re
import socket
import telnetlib
import time


def connect_and_set_command(ip, timeout=20):
    try:
        with telnetlib.Telnet(ip, timeout=timeout) as telnet:
            login = ""
            telnet.read_until(b'UserName:', timeout=5)
            telnet.write(b'username\n')
            telnet.write(b'password\n')
            login += str(telnet.read_until(b'#', timeout=5))
            telnet.write(b'\n')
            telnet.write(b'show switch\n')
            time.sleep(10)
            result = telnet.read_very_eager().decode('ascii')
            telnet.close()
            return result
    except socket.timeout:
        print("Timeout при подключении")
    except UnicodeDecodeError:
        print("Error code")
    except TypeError:
        pass


if __name__ == "__main__":

    regex = r'Device Type +: (\S+)'
    regex1 = r'Firmware Version +: Build (\S+)'
    regex2 = r'Firmware Version +: (\S+)'
    try:
        with open("ip.txt") as file:
            for ip in file:
                dev_ip = ip.rstrip()
                # print(dev_ip)
                result = connect_and_set_command(dev_ip)
                # pprint(result)
                match = re.finditer(regex, result)
                for m in match:
                    device_type = m.group(1)
                match = re.finditer(regex1, result)
                for m in match:
                    soft1 = m.group(1)
                match = re.finditer(regex2, result)
                for m in match:
                    soft2 = m.group(1)
                if device_type == 'DES-3200-18' or 'DES-3200-28F' or 'DES-3200-28':
                    print(f"{dev_ip} {device_type} {soft1}")
                else:
                    print(f"{dev_ip} {device_type} {soft2}")
    except TypeError:
        print("error")
