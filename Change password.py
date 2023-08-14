import telnetlib
import socket
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
            telnet.write(b'config account admin\n')
            telnet.write(b'Intr1X\n')
            telnet.write(b'Password_new\n')
            telnet.write(b'Password_new\n')
            telnet.write(b'save\n')
            telnet.write(b'save all\n')
            time.sleep(40)
            result = telnet.read_very_eager().decode('ascii')
            telnet.close()
            return result
    except socket.timeout:
        print("Timeout при подключении")
    except UnicodeDecodeError:
        print("Error code")

if __name__ == "__main__":

    with open("ip.txt") as file:
        for ip in file:
            dev_ip = ip.rstrip()
            print(dev_ip)
            result = connect_and_set_command(dev_ip)
            print(result)
#
#
