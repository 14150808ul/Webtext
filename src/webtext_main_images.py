#!/usr/bin/python3

import sys, configparser
from pathlib import Path
import networks, pasteboard

#create network object using factory
network = networks.network_factory('three')

#open ini file containing login details
path = str(Path.home()) + '/.webtext.ini'
config = configparser.ConfigParser()
config.read(path)

if(network.network_name not in config):
    #Must create .ini file (or add details to it)
    config_username = input( network.network_name + ' username: ')
    config_password = input( network.network_name + ' password: ')

    config[network.network_name] = { 'username' : config_username,
                        'password' : config_password }

    with open(path, 'w') as configfile:
        config.write(configfile)



username = config[network.network_name]['username']
password = config[network.network_name]['password']

recipient_number = input("Enter name or number: ")

#check if recipient starts with a digit
if not recipient_number[0].isdigit():
#look up name in contacts
    if not config.has_option('contacts', recipient_number):
        print("Cannot find contact: \"" + recipient_number +"\" in config file\nexiting")
        sys.exit()
    else:
        recipient_number = config['contacts'][recipient_number]


filename = input("Enter file name: ")

#Do validation, assume file exists for now
url = pasteboard.upload_image_file(filename)

message_text = 'You have been sent an image, to view click this link: ' + url


print("logging in to "+ network.network_homepage + "...")
login_message = network.login(username, password)
print(login_message)
if not network.logged_in:
    sys.exit()

message_array = []

while message_text:
    message_array.append(message_text[:network.char_limit])
    message_text = message_text[network.char_limit:]

for message_num, message in enumerate(message_array, start=1):
    print('sending webtext (' + str(message_num) + ' of ' + str(len(message_array)) + ')...')
    network.send_webtext(message, recipient_number)

print ("webtext sent\nRemaining texts: " + network.remaining_texts)
