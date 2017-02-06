__author__ = 'nherriot'


"""UAA Test App - python client.

UAA checks that our UAA component is:

1. Alive by doing a HTTP GET to the default port

2. Checking that it can do a HTTP GET with a constructed URL to receive OAuth tokens for a legitimate user.

3. Checking that it can do a HTTP GET with a constructed URL to receive OAuth granted for a legitimate user.

4. Checking that it can do a HTTP GET with a constructed URL to receive a failure for a user not on the system.

5. Checking UAA end point exists for xxx.

This script is nothing more that a miniature test or sanity test program for sprint1 to ensure we have a component
up and running. At some point this should be made into a test function.

"""


import requests                                 # Used to do all http requests to our nodes
from requests_toolbelt.utils import dump
import yaml                                     # Used to parse parameters from our yaml configuration files
import sys


# Fetch the correct port and domain name to talk to the UAA from the docker-compose.yml file
with open('docker-compose.yml', 'r') as f:
    dockerEnvironment = yaml.load(f)

UAAdomain = "http://127.0.0.1:"
UAAport = dockerEnvironment["services"]["ras-authentication"]["ports"][0][0:4]
UAAendPoint = "/uaa/oauth/token"
UAAurl = UAAdomain + UAAport + UAAendPoint
# print "UAAurl is: ", UAAurl



# Fetch the list of users we want to test from the uaa.yml file
myUsers =[]

with open('ras-authentication/ras-config/uaa.yml', 'r') as f:
    uaaEnvironment = yaml.load(f)

UAAusers = uaaEnvironment["scim"]["users"]
for key in UAAusers:
    user = key
    userName =  user.split("|", 1)[0]
    userPassword = user.split("|", 2)[1]
    myUsers.append((userName, userPassword))

#for key in myUsers:
#    print "Username : ", key[0]
#    print "Password : ", key[1]


# Populating data in body of the HTTP Post request

#data = {"eventType": "AAS_PORTAL_START", "data": {"uid": "hfe3hf45huf33545", "aid": "1", "vid": "1"}}

data = {"username": "paul", "password": "wallaby", "client_id": "cf", "grant_type": "password", "response_type": "token" }
params = {'sessionKey': '9ebbd0b25760557393a43064a92bae539d962103', 'format': 'xml', 'platformId': 1}
headers = {'content-type': 'Application/json'}
authorisation = ('cf', '')

print  "\n\n****************************\n***** UAA Test Program *****\n****************************"


try:
    #uaa_response = requests.get(UAAurl)
    #uaa_response = requests.post(UAAurl, params=params, json=data)
    uaa_response = requests.post(UAAurl, auth=authorisation, headers=headers, data=data)

    # Use the dump_all function for requests-toolbelt pacakge to look at exactly at our HTTP message.
    data = dump.dump_all(uaa_response)
    print "\n**********************************************\n********** Dumping our HTTP Message **********\n**********************************************"
    print(data.decode('utf-8'))


except requests.exceptions.ConnectionError:
    print "There seems to be no server listening on this connection?"

except requests.exceptions.Timeout:
    print "Timeout error"

except requests.exceptions.RequestException as e:
    # catastrophic error. bail.
    print e
    sys.exit(1)




print "\nWe are using the URL:      {}".format(uaa_response.url)
print "Response from the server:  {}".format(uaa_response.text)
print "Response encoding:         {}".format(uaa_response.encoding)
print "Raw content:               {}".format(uaa_response.content)
print "Status Code:               {}".format(uaa_response.status_code)
print "Request Headers:           {}".format(uaa_response.headers)
