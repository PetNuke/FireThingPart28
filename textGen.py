# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
import configparser


def sendMSG(msg):
    config = configparser.ConfigParser()
    config.read("configs.ini")
    config = config['text']

    account_sid = config['account_sid']
    auth_token = config['auth_token']
    client = Client(account_sid, auth_token)

    return client.messages \
                .create(
                     body=msg,
                     from_=config['sender'],
                     to=config['receiver']
                 )


# Test message
# print(sendMSG("Here is the link to the map: Bob - <a href=http://maps.google.com/maps?q=200%20W%20Dickson%20Ave+78214>banana</a>"))
