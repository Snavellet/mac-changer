import re
import subprocess
import sys
import time
from argparse import ArgumentParser

from colorama import Fore, init

init()

OS = 'linux'

if sys.platform.lower() != OS:
    print(Fore.RED + f'[-] The operating system must be {OS}.')
    time.sleep(3)
    exit()


def change_mac():
    def check_arguments():
        parser = ArgumentParser()
        parser.add_argument('-r', '--random', dest='ran',
                            help='Input "y" (without quoted) if you want to generate a random MAC address.')
        parser.add_argument('-m', '--mac', dest='mac',
                            help='You can set your own MAC address in the ff:ff:ff:ff:ff:ff format.')
        parser.add_argument('-i', '--interface', dest='interface', help='The interface to change the MAC address.')

        args = parser.parse_args()
        return args

    def check_valid(args):
        try:
            if args.interface:
                if args.mac and args.ran:
                    print(Fore.RED + '[-] Please provide only one argument between -r and -m.')
                    time.sleep(3)
                    exit()
                else:
                    service_manager_stop = 'service network-manager stop &> /dev/null'
                    service_manager_start = 'service network-manager start &> /dev/null'

                    if args.mac:
                        valid_mac = re.search(r'\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2}', args.mac)

                        if valid_mac is None:
                            print(Fore.RED + '[-] Invalid MAC address format, add -h for more info.')
                            time.sleep(3)
                            exit()
                        else:
                            mac_address = args.mac
                            interface = args.interface

                            subprocess.Popen(f'ifconfig {interface} down', shell=True)
                            subprocess.Popen(service_manager_stop, shell=True)

                            output = ''
                            try:
                                output = subprocess.check_output(f'macchanger --mac={mac_address} {interface}',
                                                                 shell=True)
                            except subprocess.CalledProcessError:
                                time.sleep(2)
                                subprocess.Popen(service_manager_start, shell=True)
                                print(
                                    Fore.RED + f'[-] MAC Address change failed! You are changing to the same MAC address you are currently using.')
                                time.sleep(3)
                                exit()
                            time.sleep(2)
                            subprocess.Popen(service_manager_start, shell=True)
                            subprocess.Popen(f'ifconfig {interface} up', shell=True)

                            all_mac = re.findall(r'(MAC:\s+)(\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2})',
                                                 output.decode('utf8'))

                            mac_addresses = []

                            for mac_address in all_mac:
                                mac_addresses.append(mac_address[1])

                            if mac_addresses[0] != mac_addresses[2]:
                                print(
                                    Fore.GREEN + f'[+] MAC Address has been changed to {mac_addresses[2]} successfully!')
                                time.sleep(3)
                                exit()
                            else:
                                print(Fore.RED + f'[-] MAC Address change failed!')
                                time.sleep(3)
                                exit()

                    if args.ran == 'y':
                        interface = args.interface

                        subprocess.Popen(f'ifconfig {interface} down', shell=True)
                        subprocess.Popen(service_manager_stop, shell=True)
                        output = subprocess.check_output(f'macchanger -r {interface}', shell=True)
                        time.sleep(2)
                        subprocess.Popen(service_manager_start, shell=True)
                        subprocess.Popen(f'ifconfig {interface} up', shell=True)

                        all_mac = re.findall(r'(MAC:\s+)(\w{2}:\w{2}:\w{2}:\w{2}:\w{2}:\w{2})', output.decode('utf8'))

                        mac_addresses = []

                        for mac_address in all_mac:
                            mac_addresses.append(mac_address[1])

                        if mac_addresses[0] != mac_addresses[2]:
                            print(Fore.GREEN + f'[+] MAC Address has been changed to {mac_addresses[2]} successfully!')
                            time.sleep(3)
                            exit()
                        else:
                            print(Fore.RED + f'[-] MAC Address change failed!')
                            time.sleep(3)
                            exit()
                    else:
                        print(Fore.RED + f'[-] Please add -h for more info!')
                        time.sleep(3)
                        exit()
            else:
                print(Fore.RED + f'[-] Please input the interface, add -h for more info!')
                time.sleep(3)
                exit()
        except KeyboardInterrupt:
            exit()

    check_valid(check_arguments())


if __name__ == '__main__':
    change_mac()
