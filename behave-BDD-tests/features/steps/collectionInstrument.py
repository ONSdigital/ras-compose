__author__ = 'nherriot'

"""CI Micro Service.

This checks that the Collection Instrument can:

1. Report it's own status.

2. Provide a json object of 'collection data' given a collection ID with 'sunny day' scenario values.

3. Report 'data not available' when a collection instrument index is not in the DB.

4. Allow new collection instruments to be added by an CEC admin user ( a user with the correct scope ).

5. Refuse to allow a new collection instrument to be added with a user 'Respondent' who does not have the correct scope.

6. Report an out of bounds error for values that are not within range when 'POST'ing data. i.e. boundary conditions.

7. Send a user to the UAA if they HTTP request sent to the CI does not have a valid authentication token.

To run:
/>  behave collectionInstrument.py

"""

import requests
from behave import *


@given('The CI status is active')
def step_impl(context):
   CIdomain = "http://127.0.0.1:"
   CIport = "8070"
   CIendpoint = "/status"
   CIurl = CIdomain + CIport + CIendpoint
   print ("    *** The URL to go to is:" + CIurl + " \n")
   context.response = requests.get(CIurl)



@when('A request for status is given')
def step_impl(context):
   print ("    *** HTT Response code is:", context.response.status_code, " \n\n")
   assert context.response.status_code == 200


@then('The CI micro service returns status information about itself')
def step_impl(context):
   print ("    *** Response is: ", context.response.text, "\n")
   assert context.response.text == "Collection Instrument service is running"

