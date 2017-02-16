__author__ = 'nherriot'


"""UAA Test App - python client.

UAA checks that our UAA component is:

1. Alive by doing a HTTP GET to the default port

2. Checking that it can do a HTTP GET with a constructed URL to receive OAuth tokens for a legitimate user.

3. Checking that it can do a HTTP GET with a constructed URL to receive OAuth granted for a legitimate user.

4. Checking that it can do a HTTP GET with a constructed URL to receive a failure for a user not on the system.

5. Checking UAA end point exists for xxx.

TODO: This script is nothing more that a miniature test or sanity test program for sprint1 to ensure we have a component
up and running. At some point this should be made into a test function.

To run:
/>  python uaa-test.py

"""


import requests                                 # Used to do all http requests to our nodes
from requests_toolbelt.utils import dump        # Used when printing http debug to the screen
import yaml                                     # Used to parse parameters from our yaml configuration files
import sys


# Creating colours to use when printing things to the screen
class Bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# A small helper function to allow us to check the status codes from our HTTP requests.
def checkResponseCodes(http_status_code):

    if http_status_code >= 200 and http_status_code < 300:
        print Bcolors.OKGREEN + "** Success From Server " + str(http_status_code) + " **" + Bcolors.ENDC
    else:

        if http_status_code >= 300 and http_status_code < 400:
            print Bcolors.WARNING + "** Server has redirected us to a different URL " + str(http_status_code) + " **" + Bcolors.ENDC
        else:

            if http_status_code >=400 and http_status_code < 500:
                print Bcolors.FAIL + "** Server has reported a client error of: " + str(http_status_code) + " **" + Bcolors.ENDC
            else:
                print Bcolors.FAIL + "** Server error of: " + http_status_code + " **" + Bcolors.ENDC






print  "\n\n****************************\n***** UAA Test Program *****\n****************************"


# Fetch the correct port and domain name to talk to the UAA from the docker-compose.yml file
with open('docker-compose.yml', 'r') as f:
    dockerEnvironment = yaml.load(f)

UAAdomain = "http://127.0.0.1:"
UAAport = dockerEnvironment["services"]["ras-authentication"]["ports"][0][0:4]
UAAendPoint = "/uaa/oauth/token"
UAAurl = UAAdomain + UAAport + UAAendPoint
print Bcolors.OKBLUE + "\n*** Found UAA Config from docker-compose.yml. UAAurl is: " + UAAurl + " OK ***" + Bcolors.ENDC



# Fetch the list of users we want to test from the uaa.yml file
myUsers =[]                                                         # Just an empty list to populate

with open('ras-authentication/ras-config/uaa.yml', 'r') as f:
    uaaEnvironment = yaml.load(f)

UAAusers = uaaEnvironment["scim"]["users"]
for key in UAAusers:
    userName =  key.split("|", 1)[0]
    userPassword = key.split("|", 2)[1]
    myUsers.append((userName, userPassword))

print Bcolors.OKBLUE + "\n*** Found UAA Users Config from uaa.yml  OK ***" + Bcolors.ENDC
for key in myUsers:
    print "Username : ", key[0], "     Password : ", key[1]



# Populating data in body of the HTTP Post request

data = {"username": "stefan", "password": "wallaby", "client_id": "cf", "grant_type": "password", "response_type": "token" }
params = {'sessionKey': '9ebbd0b25760557393a43064a92bae539d962103', 'format': 'xml', 'platformId': 1}
#headers = {'content-type': 'Application/json'}
#headers = {"Connection": "close"}
headers = {'content-type': 'application/x-www-form-urlencoded'}
authorisation = ('cf', '')


print  "\n\n****************************\n****** Starting Test  ******\n**** Check Server Is OK ***q*\n****************************"

try:
    #uaa_response = requests.post(UAAurl, params=params, json=data)s = requests.session()

    UAAbaseUrl = UAAdomain + UAAport
    uaa_response = requests.get(UAAbaseUrl)
    print "\nWe are using the URL:      {}".format(uaa_response.url)
    checkResponseCodes(uaa_response.status_code)
    #HttpResponseDictionary = uaa_response.json()

    if uaa_response.status_code==200:
        print Bcolors.OKGREEN + "*** Test Passed OK ***" + Bcolors.ENDC
    else:
        print Bcolors.FAIL + "*** Test Failed ***" + Bcolors.ENDC

except requests.exceptions.ConnectionError:
    print Bcolors.FAIL + "There seems to be no server listening on this connection?" + Bcolors.ENDC

except requests.exceptions.Timeout:
    print Bcolors.FAIL + "Timeout error"  + Bcolors.ENDC

except requests.exceptions.RequestException as e:
    # catastrophic error. bail.
    print Bcolors.FAIL + e + Bcolors.ENDC
    sys.exit(1)




print  "\n\n****************************\n****** Starting Test  ******\n*** authenticating users ***\n****************************"

for key in myUsers:

    data['username'] = key[0]
    data['password'] = key[1]
    print "\nUsername is now: " + data['username']

    try:
        #uaa_response = requests.post(UAAurl, params=params, json=data)s = requests.session()

        uaa_response = requests.post(UAAurl, auth=authorisation, headers=headers, data=data)
        print "\nWe are using the URL:      {}".format(uaa_response.url)
        checkResponseCodes(uaa_response.status_code)
        HttpResponseDictionary = uaa_response.json()

        if 'access_token' in HttpResponseDictionary:
#            print "Got access token of: " + Bcolors.BOLD + HttpResponseDictionary['access_token'][0:10] + " ...... " + HttpResponseDictionary['access_token'][-10:] + Bcolors.ENDC
            print "Got access token of: " + Bcolors.BOLD + HttpResponseDictionary['access_token'] + " ...... " + HttpResponseDictionary['access_token'][-10:] + Bcolors.ENDC
            print "Got token type of: " + Bcolors.BOLD + HttpResponseDictionary['token_type'] + Bcolors.ENDC
 #           print "Got refresh token of:" + Bcolors.BOLD + HttpResponseDictionary['refresh_token'][0:10] + " ...... " + HttpResponseDictionary['refresh_token'][-10:] + Bcolors.ENDC
            print "Got refresh token of:" + Bcolors.BOLD + HttpResponseDictionary['refresh_token'] + " ...... " + HttpResponseDictionary['refresh_token'][-10:] + Bcolors.ENDC
            print "The refresh token expires in: " + Bcolors.BOLD +str(HttpResponseDictionary['expires_in']) + Bcolors.ENDC
            print "Got scope of: " + Bcolors.BOLD + HttpResponseDictionary['scope'] + Bcolors.ENDC
            print Bcolors.OKGREEN + "*** Test Passed OK ***" + Bcolors.ENDC

        if 'error' in HttpResponseDictionary:
            print "Error is: " + Bcolors.BOLD + HttpResponseDictionary['error'] + Bcolors.ENDC
            print "Error description is: " + Bcolors.BOLD + HttpResponseDictionary['error_description'] + Bcolors.ENDC
            print Bcolors.FAIL + "*** Test Failed ***" + Bcolors.ENDC

        # Use the dump_all function for requests-toolbelt pacakge to look at exactly at our HTTP message.
        #
        # data = dump.dump_all(uaa_response)
        #print "\n**********************************************\n********** Dumping our HTTP Message **********\n**********************************************"
        #print(data.decode('utf-8'))

    except requests.exceptions.ConnectionError:
        print Bcolors.FAIL + "There seems to be no server listening on this connection?" + Bcolors.ENDC

    except requests.exceptions.Timeout:
        print Bcolors.FAIL + "Timeout error"  + Bcolors.ENDC

    except requests.exceptions.RequestException as e:
        # catastrophic error. bail.
        print Bcolors.FAIL + e + Bcolors.ENDC
        sys.exit(1)


print  "\n\n****************************\n****** Starting Test  ******\n******* illegal user *******\n****************************"

data['username'] = "nobody"
data['password'] = myUsers[0][1]
print "\nUsername is now: " + data['username']

try:
    #uaa_response = requests.post(UAAurl, params=params, json=data)s = requests.session()

    uaa_response = requests.post(UAAurl, auth=authorisation, headers=headers, data=data)
    print "\nWe are using the URL:      {}".format(uaa_response.url)
    checkResponseCodes(uaa_response.status_code)
    HttpResponseDictionary = uaa_response.json()

    if 'access_token' in HttpResponseDictionary:
        print "Got access token of: " + Bcolors.BOLD + HttpResponseDictionary['access_token'][0:10] + " ...... " + HttpResponseDictionary['access_token'][-10:] + Bcolors.ENDC
        print "Got token type of: " + Bcolors.BOLD + HttpResponseDictionary['token_type'] + Bcolors.ENDC
        print "Got refresh token of:" + Bcolors.BOLD + HttpResponseDictionary['refresh_token'][0:10] + " ...... " + HttpResponseDictionary['refresh_token'][-10:] + Bcolors.ENDC
        print "The refresh token expires in: " + Bcolors.BOLD +str(HttpResponseDictionary['expires_in']) + Bcolors.ENDC
        print "Got scope of: " + Bcolors.BOLD + HttpResponseDictionary['scope'] + Bcolors.ENDC
        print Bcolors.FAIL + "*** Test Passed OK ***" + Bcolors.ENDC

    if 'error' in HttpResponseDictionary:
        print "Error is: " + Bcolors.BOLD + HttpResponseDictionary['error'] + Bcolors.ENDC
        print "Error description is: " + Bcolors.BOLD + HttpResponseDictionary['error_description'] + Bcolors.ENDC
        print Bcolors.OKGREEN + "*** Test Passed ***" + Bcolors.ENDC

    # Use the dump_all function for requests-toolbelt pacakge to look at exactly at our HTTP message.
    #
    # data = dump.dump_all(uaa_response)
    #print "\n**********************************************\n********** Dumping our HTTP Message **********\n**********************************************"
    #print(data.decode('utf-8'))

except requests.exceptions.ConnectionError:
    print Bcolors.FAIL + "There seems to be no server listening on this connection?" + Bcolors.ENDC

except requests.exceptions.Timeout:
    print Bcolors.FAIL + "Timeout error"  + Bcolors.ENDC

except requests.exceptions.RequestException as e:
    # catastrophic error. bail.
    print Bcolors.FAIL + e + Bcolors.ENDC
    sys.exit(1)




print  "\n\n****************************\n****** Starting Test  ******\n****** Wrong Password ******\n****************************"

data['password'] = "xxxxxxxxxx"
data['username'] = myUsers[0][0]
print "\nPassword is now: " + data['password']

try:
    #uaa_response = requests.post(UAAurl, params=params, json=data)s = requests.session()

    uaa_response = requests.post(UAAurl, auth=authorisation, headers=headers, data=data)
    print "\nWe are using the URL:      {}".format(uaa_response.url)
    checkResponseCodes(uaa_response.status_code)
    HttpResponseDictionary = uaa_response.json()

    if 'access_token' in HttpResponseDictionary:
        print "Got access token of: " + Bcolors.BOLD + HttpResponseDictionary['access_token'][0:10] + " ...... " + HttpResponseDictionary['access_token'][-10:] + Bcolors.ENDC
        print "Got token type of: " + Bcolors.BOLD + HttpResponseDictionary['token_type'] + Bcolors.ENDC
        print "Got refresh token of:" + Bcolors.BOLD + HttpResponseDictionary['refresh_token'][0:10] + " ...... " + HttpResponseDictionary['refresh_token'][-10:] + Bcolors.ENDC
        print "The refresh token expires in: " + Bcolors.BOLD +str(HttpResponseDictionary['expires_in']) + Bcolors.ENDC
        print "Got scope of: " + Bcolors.BOLD + HttpResponseDictionary['scope'] + Bcolors.ENDC
        print Bcolors.FAIL + "*** Test Passed OK ***" + Bcolors.ENDC

    if 'error' in HttpResponseDictionary:
        print "Error is: " + Bcolors.BOLD + HttpResponseDictionary['error'] + Bcolors.ENDC
        print "Error description is: " + Bcolors.BOLD + HttpResponseDictionary['error_description'] + Bcolors.ENDC
        print Bcolors.OKGREEN + "*** Test Passed ***" + Bcolors.ENDC

    # Use the dump_all function for requests-toolbelt pacakge to look at exactly at our HTTP message.
    #
    # data = dump.dump_all(uaa_response)
    #print "\n**********************************************\n********** Dumping our HTTP Message **********\n**********************************************"
    #print(data.decode('utf-8'))

except requests.exceptions.ConnectionError:
    print Bcolors.FAIL + "There seems to be no server listening on this connection?" + Bcolors.ENDC

except requests.exceptions.Timeout:
    print Bcolors.FAIL + "Timeout error"  + Bcolors.ENDC

except requests.exceptions.RequestException as e:
    # catastrophic error. bail.
    print Bcolors.FAIL + e + Bcolors.ENDC
    sys.exit(1)

