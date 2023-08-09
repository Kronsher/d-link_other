import telnetlib
import socket
import time


def connect_and_set_command(ip, timeout=20):
    try:
        with telnetlib.Telnet(ip, timeout=timeout) as telnet:
            login = ""
            telnet.read_until(b'UserName:', timeout=5)
            telnet.write(b'admin\n')
            telnet.write(b'Intr1X\n')
            login += str(telnet.read_until(b'#', timeout=5))
            telnet.write(b'\n')
            telnet.write(b'enable ssh\n')
            telnet.write(b'create authen server_host 192.168.112.42 protocol tacacs+ port 49 key "Intr0neX" timeout 5 retransmit 2\n')
            telnet.write(b'config authen server_group tacacs+ add server_host 192.168.112.42 protocol tacacs+\n')
            telnet.write(b'create authen_login method_list_name tac\n')
            telnet.write(b'config authen_login method_list_name tac method tacacs+\n')
            telnet.write(b'create authen_enable method_list_name tac_en\n')
            telnet.write(b'config authen_enable method_list_name tac_en method tacacs+\n')
            telnet.write(b'config authen application telnet login method_list_name tac\n')
            telnet.write(b'config authen application telnet enable method_list_name tac_en\n')
            telnet.write(b'enable authen_policy\n')
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
