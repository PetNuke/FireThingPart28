import pandas as pd
import configparser
from bs4 import BeautifulSoup
import requests
from emailGen import sendEmail
import datetime
import os
import sys


def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        # Running in PyInstaller bundle
        base_path = sys._MEIPASS
    else:
        # Running in a normal Python environment
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


print("running program at", datetime.datetime.now())


# Use get_resource_path() to get the full path to your resource files
configs_path = get_resource_path("configs.ini")
html_message_path = get_resource_path("htmlMessage.txt")

# Use configparser to read the configuration file
config = configparser.ConfigParser()
config.read(configs_path)
url = config['default']['url']


# !NOTICE! links have some text connect by spaces, but it is all one link
def getLinks():
    response = requests.get(url)
    html = response.content

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table')

    location_links = []

    for link in table.find_all('a'):
        href = link.get('href')
        if href and '//maps' in href:
            location_links.append(href.replace(" ", ""))

    return location_links


# puts website data into data frame
dfs = pd.read_html(url)
df = dfs[1]
df.fillna(-1, inplace=True) # replaces nan values with -1

# Adds Address links
df = df.assign(addrLink=getLinks())

# Blacklist
unwanted = eval(config['default']['blacklist'])
for x in unwanted:
    mask = df['Problem Type'].str.contains(x)
    df = df.drop(index=df[mask].index, axis=0)


# Remove fires not in a certain time limit
df['Response Time'] = pd.to_datetime(df['Response Time'])
currentTime = pd.Timestamp.now()
timeDelta = pd.Timedelta(minutes=15)
mask = df['Response Time'] <= currentTime - timeDelta
df = df[~mask]

df = df.reset_index()


# Gets the message framework
# fout = open('messageFrame.txt')
fout = open(html_message_path)
frame = fout.read()

# Sends the messages
emails = eval(config['email']['receiver_email'])

for i in range(df.shape[0]):
    for send in emails:
        # print(sendMSG(frame.format(df['Response Time'][i], df['Problem Type'][i], df['Addrs'][i], df['Cross Street'][i], df['ZipCode'][i], df['# of Units'][i], df['TAC'][i], df['addrLink'][i])))
        sendEmail("Fire Report", frame.format(df['Response Time'][i], df['Problem Type'][i], df['Addrs'][i], df['Cross Street'][i], df['ZipCode'][i], df['# of Units'][i], df['TAC'][i], df['addrLink'][i]), send)

# The Columns are Index(['index', '# of Units', 'Response Time', 'Problem Type', 'Addrs',
#        'Cross Street', 'Location Type', 'ZipCode', 'TAC', 'addrLink'],
#       dtype='object')
