#!/usr/bin/env python3

import os
import sys
import subprocess
import time

#if the library requests is not installed, install it via pip
try:
    import requests
except ImportError:
    print("[!] The requests library is not installed. Installing...")
    os.system("pip install requests")
    time.sleep(1)
    #tell the user the library is installed
    print("[!] The requests library is now installed")
    #tell the user to please restart the program
    print("Please restart the program")
    time.sleep(3)
    sys.exit()

#if the library tqdm is not installed, install it via pip
try:
    from tqdm import tqdm
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", "tqdm"])
     #tell the user the library is installed
    print("[!] The tqdm library is now installed")
    #tell the user to please restart the program
    print("Please restart the program")
    time.sleep(3)
    sys.exit()

# If the library csv is not installed, install it via pip
try:
    import csv
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", "csv"])
    print("[!] The csv library is now installed")
    print("Please restart the program")
    time.sleep(3)
    sys.exit()

#If the rich library is not installed, install it via pip
try:
    from rich import print
    from rich.columns import Columns
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", "rich"])
    import rich
    time.sleep (1)
     #tell the user the library is installed
    print("[!] Rich module is now installed")
    print("Please restart the program")
    time.sleep(3)
    sys.exit()


mac_list = [] #Create an empty list to store the MAC addresses
port_list = [] #Create an empty list to store the Ports 
vendor_list = [] #Create an empty list to store the vendor names
total_list = [] #create a list to store the mac addresses, ports, and vendor names

#Store the current directory in a variable named path
path = os.getcwd()

#Show the current directory and a list of its contents
def print_dir_contents(path):
    print("\nCurrent Directory:[cyan]" + path + "[/cyan]")
    print("\nDirectory Contents:")
    for item in os.listdir(path):
        print("[green]"+ item + "[/green]")

#Call the print_dir_contents function to print the contents of the current directory
print_dir_contents(path)

#Ask the user to pick a MAC address file to search from the current directory, if the file doesn't exist, ask the user to enter a valid file
while True:
    MAC_FILE = input("\nPlease select a file to search: ")
    if os.path.isfile(MAC_FILE):
        break
    else:
        print("\nInvalid file name. Please try again.")

#Ask the user which column is the MAC address column
print("\nPlease select the [cyan]MAC Address[/cyan] Column to search from the MAC address file: ")
COLUMN = input("> ")
COLUMN = int(COLUMN)
COLUMN = COLUMN - 1

#Ask the user which column is the ports column
print("\nPlease select the [cyan]Ports[/cyan] Column to search from the MAC address file: ")
PORTS = input("> ")
PORTS = int(PORTS)
PORTS = PORTS - 1

#read the MAC_file line by line
with open(MAC_FILE) as f:
    for line in f:
        #Split the line into words using the split() method
        words = line.split()
        #Append the MAC address to the mac_list
        mac_list.append(words[COLUMN])
        port_list.append(words[PORTS])

#Go through the mac_list and if an element starts with "Mac" remove it from the list
for element in mac_list:
    if element.startswith("Mac"):
        mac_list.remove(element)

#Go through the mac_list and if an element starts with "---" remove it from the list
for element in mac_list:
    if element.startswith("--"):
        mac_list.remove(element)

#Go through the PORTS list and if an element starts with "Ports" remove it from the list
for element in port_list:
    if element.startswith("Ports"):
        port_list.remove(element)

#Go through the PORTS list and if an element starts with "---" remove it from the list
for element in port_list:
    if element.startswith("--"):
        port_list.remove(element)

#Go through the mac_list and make every element uppercase
for element in mac_list:
    element = element.upper()

#Use the requests library to get the vendor name of the mac address
def get_vendor_name(mac_address):
    #try to get the vendor name from the mac address for 2 seconds
    try:
        response = requests.get("https://macvendors.co/api/vendorname/" + mac_address, timeout=2)
        #If the response is successful, return the vendor name
        if response.status_code == 200:
            return response.text
        #If the response is not successful, return the error code
        else:
            return response.status_code
    #If the response times out, return the error code
    except requests.exceptions.Timeout:
        return "Timeout"

print("\n[yellow]===[/yellow] Please wait while the vendors are being collected [yellow]===[/yellow]\n")   

#Go through the mac_list and get the vendor name of each mac address, using tqdm to show progress
for element in tqdm(mac_list):
    mac_address = element
    vendor_name = get_vendor_name(mac_address)
    vendor_list.append(vendor_name)

#for every element in the mac_list, print the element the corresponding port and vendor name
print("\nHere is the information for the MAC addresses:\n")
for element in mac_list:
    columns = Columns([element, port_list[mac_list.index(element)], vendor_list[mac_list.index(element)]], padding= (0,4))
    try:
        print(columns)
    except UnicodeEncodeError:
        pass
    
#Save the mac_list, port_list, and vendor_list to a csv file separated by commas to a file name of the current date and time.csv
with open(time.strftime("%Y-%m-%d") + ".csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["MAC Address", "Port", "Vendor Name"])
    writer.writerows(zip(mac_list, port_list, vendor_list))
#close the file
f.close()

#Tell the user that a csv file has been created
print("\nA csv file has been created with the current date and time as the name.")
#Create a countdown timer that prints the time every second until the timer reaches 0
def countdown_timer():
    #set the timer to 10 seconds
    timer = 3
    #while loop to run the timer
    while timer > 0:
        #print the timer every second
        print(str(timer), end=" ".rstrip("\n"),)
        time.sleep(1)
        #decrement the timer by 1
        timer -= 1
    print("...", end="".rstrip("\n"))
#Say the to the user that program will exit in 3 seconds, call the countdown_timer function
print("\nProgram will exit in 3 seconds.")
countdown_timer()
sys.exit()



