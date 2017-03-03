__author__ = 'ltoozer'

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




before_tag(context, tag), after_tag(context, tag)
These run before and after a section tagged with the given name. They are invoked for each tag
encountered in the order they’re found in the feature file. See controlling things with tags.
"""

import requests
# import psycopg2
from behave import *
from jsonschema import validate
import ast


@given('The CI status is active')
def step_impl(context):
    CIendpoint = "/status"
    CIurl = context.CIdomain + context.CIport + CIendpoint
    print ("    *** The URL to go to is:" + CIurl + " \n")
    context.response = requests.get(CIurl)


@when('A request for status is given')
def step_impl(context):
    print ("    *** HTTP Response code is:", context.response.status_code, " \n\n")
    assert context.response.status_code == 200


@then('The CI micro service returns status information about itself')
def step_impl(context):
    print ("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == "Collection Instrument service is running"



@given('a valid collection instrument ID')
def step_impl(context):
   context.cursor.execute(
       "SELECT content "
       "FROM ras_collection_instruments "
       "LIMIT 1"
   )
   content_row = context.cursor.fetchone()
   context.collection_instrument_id = content_row[0]['id']


@when('a request is made for the collection instrument data')
def step_impl(context):
    CIendpoint = "/collectioninstrument/id/"

    url = context.CIdomain + context.CIport + CIendpoint + context.collection_instrument_id
    print("    *** The URL to go to is: " + url + " \n")
    context.response = requests.get(url)
    assert context.response.status_code == 200
    assert context.response.headers['Content-Type'] == 'collection/json'


@then('check the returned data is correct')
def step_impl(context):
    schema_definition = {
        "type": "object",
        "properties": {
            "reference": {"type": "string"},
            "id": {"type": "string"},
            "surveyId": {"type": "string"},
            "ciType": {"type": "string"},
            "classifiers": {
                "type": "object",
                "properties": {
                    "LEGAL_STATUS": {"type": "string"},
                    "INDUSTRY": {"type": "string"}
                }
            }
        }
    }
    # TODO: Is there a way to ensure all keys are present as well?
    # TODO: Currently, the response is in unicode - do we need to validate in ASCII?
    response_text = ast.literal_eval(context.response.text)
    response_json = response_text[0]
    validate(response_json, schema_definition)



@given('an incorrect collection instrument ID')
def step_impl(context):
    context.CI_ID = "this:is:a:bad:CI:ID"
    print ("    *** The invalid CI ID is: " + context.CI_ID + " \n")


@when('a request is made for the collection instrument data using this ID')
def step_impl(context):
    CIendpoint = "/collectioninstrument/id/"
    CIurl = context.CIdomain + context.CIport + CIendpoint + context.CI_ID
    print("    *** The URL to go to is:" + CIurl + " \n")
    context.response = requests.get(CIurl)
    assert context.response.status_code == 400


@then('information is returned saying the ID is invalid')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'Invalid ID supplied'


# **********************************************************************************************************************
# ***************************** TODO Invent how to split up our test cases for readability *****************************
# **********************************************************************************************************************

@given('a collection instrument that does not exist')
def step_impl(context):
    context.cursor.execute("SELECT content "
                  "FROM ras_collection_instruments "
                  "LIMIT 1")
    content_row = context.cursor.fetchone()
    id_section = content_row[0]['id'].split('.')

    # Replace the ID suffix with an invalid number e.g. '99999' (assuming it won't ever be this high!)
    id_section[-1] = len(id_section[-1]) * '9'

    context.collection_instrument_id = '.'.join(id_section)
    print('    *** The CI to find is: ' + context.collection_instrument_id)


@when('a request is made for the collection instrument data using its ID')
def step_impl(context):
    CIendpoint = "/collectioninstrument/id/"
    CIurl = context.CIdomain + context.CIport + CIendpoint + context.collection_instrument_id
    print("    *** The URL to go to is:" + CIurl + " \n")
    context.response = requests.get(CIurl)
    assert context.response.status_code == 404


@then('information is returned saying the collection instrument is not found')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'Collection instrument not found'



@given('a new collection instrument')
def step_impl(context):
    context.new_CI = {
        "reference": "test-collection-instrument",
        "surveyId": "urn:ons.gov.uk:id:survey:001.001.00001",
        "id": "urn:ons.gov.uk:id:ci:001.001.00001",
        "ciType": "OFFLINE",
        "classifiers": {
            "RU_REF": "01234567890"
        }
    }


@when('a request is made to create the collection instrument')
def step_impl(context):
    CIendpoint = "/collectioninstrument"
    CIurl = context.CIdomain + context.CIport + CIendpoint
    print("    *** The URL to go to is: " + CIurl + "\n")
    headers = {'Content-type': 'application/json'}
    context.response = requests.post(CIurl, json=context.new_CI, headers=headers)
    assert context.response.status_code == 201


@then('the collection instrument is created successfully')
def step_impl(context):
    pass