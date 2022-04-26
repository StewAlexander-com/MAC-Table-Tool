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

#if the tabular library is not installed, install it via pip
try:
    from tabulate import tabulate
except ImportError:
    subprocess.call([sys.executable, "-m", "pip", "install", "tabulate"])
    print("[!] The tabular library is now installed")
    print("Please restart the program")
    time.sleep(3)
    sys.exit()

mac_list = [] #Create an empty list to store the MAC addresses
port_list = [] #Create an empty list to store the Ports 
vendor_list = [] #Create an empty list to store the vendor names
total_list = [] #create a list to store the mac addresses, ports, and vendor names

print('''[bright_blue]
##     ##    ###     ######  ######## ########  #######   #######  ##       
###   ###   ## ##   ##    ##    ##       ##    ##     ## ##     ## ##       
#### ####  ##   ##  ##          ##       ##    ##     ## ##     ## ##       
## ### ## ##     ## ##          ##       ##    ##     ## ##     ## ##       
##     ## ######### ##          ##       ##    ##     ## ##     ## ##       
##     ## ##     ## ##    ##    ##       ##    ##     ## ##     ## ##       
##     ## ##     ##  ######     ##       ##     #######   #######  ######## 
[/bright_blue]''')


print('''[yellow]
 ┌────────────────────────────────────────────────────┐
 │  [bright_white]This program takes the output of a MAC[/bright_white]            |
 |  [bright_white]Hardware Address Table command and[/bright_white]                |
 |  [bright_white]produces a csv file with 3 columns:[/bright_white]               |
 |  [bright_red]1st column: [cyan]MAC Address[/cyan][/bright_red]                           |
 |  [bright_red]2nd column: [cyan]Port / IP[/cyan][/bright_red]                             |
 |  [bright_red]3rd column: [cyan]Vendor Name[/cyan][/bright_red]                           |
 │  [yellow]                                                  │
 └────────────────────────────────────────────────────┘[/yellow]\n''')


#Store the current directory in a variable named path
path = os.getcwd()

#Show the current directory and a list of its contents
def print_dir_contents(path):
    print("\nCurrent Directory:[blue]" + path + "[/blue]")
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
print("\nPlease select the [bright_cyan]MAC Address[/bright_cyan] Column to search from the MAC address or ARP file: ")
COLUMN = input("> ")
COLUMN = int(COLUMN)
COLUMN = COLUMN - 1

#Ask the user which column is the ports or IP column
print("\nPlease select the [bright_green]Ports[/bright_green] (or [bright_green]IP[/bright_green] Address) Column to search from the MAC address file: ")
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

for element in vendor_list:
    #change the element to a string
    element = str(element)
    
print("\nCreating the [bright_red]CSV[/bright_red] file...")
    
#Save the mac_list, port_list, and vendor_list to a csv file separated by commas to a file name of the current date and time.csv
with open(time.strftime("%Y-%m-%d") + ".csv", "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["MAC Address", "Port", "Vendor Name"])
    writer.writerows(zip(mac_list, port_list, vendor_list))
#close the file
f.close()

#use the tabulate library to print the first 30 rows of the mac_list, port_list, and vendor_list to a table
print("\n[yellow]===[/yellow] The first few ports within the [bright_red]CSV[/bright_red] file are: [yellow]===[/yellow]\n")
#Print the table if port_list does not contain the element "CPU" or Vendor Name does not contain the element "No vendor"
for element in range(0, 30):
    if "CPU" not in port_list[element] and "No vendor" not in vendor_list[element]:
        print(tabulate([[mac_list[element], port_list[element], vendor_list[element]]], headers=["MAC Address", "Port", "Vendor Name"], tablefmt="fancy_grid"))
    else:
        continue


#Tell the user that a csv file has been created
print("\nA csv file with the complete output has been created with the current date and time as the name.")
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



