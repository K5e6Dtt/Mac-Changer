#!/usr/bin/python3
#Needs root privilege
#Only works in Linux

import subprocess,argparse,sys,re,random
from termcolor import colored

def get_arguments():
    parser = argparse.ArgumentParser(description="A tool for changing mac addresses, If mac not given the script will generate a random mac")
    parser.add_argument('-i','--interface',dest="interface",help="The network interface")
    parser.add_argument('-m','--mac',dest="mac",help="The new MAC addresses")
    options = parser.parse_args()
    if not options.interface:
        print(colored(f"Give interface to change it's mac.\nType {sys.argv[0]} --help or -h for usage.",'red'))
        sys.exit(0)
    else:
        return options

def mac_len_checker(mac):
    if len(mac) != 17:
        print(colored("[-] Insufficient number of characters in the mac address, try with a full mac address.",'red'))
        sys.exit(0)   


def rand_mac():
    mac =  "%02x:%02x:%02x:%02x:%02x:%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
        )
    return mac


def mac_checker(interface):
    mac_address_result = subprocess.check_output(['ifconfig',interface])
    mac = mac_address_result.decode()
    mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",mac)
    mac = mac.group(0)
    return mac

def mac_changer(interface,mac):
    print(colored(f"[+] Changing MAC address to {mac}",'green'))
    subprocess.call(['ifconfig',interface,'down'])
    subprocess.call(['ifconfig',interface,'hw','ether',mac])
    subprocess.call(['ifconfig',interface,'up'])


def main():
    options = get_arguments()
    interface = options.interface
    if options.mac:
        mac = options.mac
    else:
        mac = rand_mac()    
    mac_len_checker(mac)
    try:    
        before_change = mac_checker(interface)
        mac_changer(interface,mac)
        after_change = mac_checker(interface)
        if before_change != after_change:
            print(colored("[+] MAC address changed successfully.",'green'))
        else:
            print(colored("[-] MAC is same,something went wrong please try again",'red'))
    except:
        print(colored("Error! Incorrect interface!!!",'red'))
        

if __name__ == '__main__':
    main()






