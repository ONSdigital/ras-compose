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




TODO:
-   Lots of repetition inside then/when steps for GET - can these be moved to a common function or something similar?

-   Only using a basic implementation of (jsonschema) validate. Could we validate on things like missing key, value length etc?

-   Dynamically created collection instruments used in some tests are dependent on schema data being available in db. Is this
    the best way to test, or do things need to be hard-coded instead?

-   Do POST requests need to remove any rows created in schema after a scenario?

"""

import requests
from behave import *
from jsonschema import validate
import ast

# **********************************************************************************************************************
# Scenario: CI Status Running
# **********************************************************************************************************************
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



# **********************************************************************************************************************
# Scenario: Obtain Collection Instrument data
# **********************************************************************************************************************
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
    assert context.response.headers['Content-Type'] == 'collection+json'


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
    response_text = ast.literal_eval(context.response.text)
    response_json = response_text[0]
    validate(response_json, schema_definition)


# **********************************************************************************************************************
# Scenario: Collection Instrument ID domain name is incorrect
# **********************************************************************************************************************
@given('a collection instrument ID with an incorrect domain name')
def step_impl(context):
    incorrect_domain_name = "ons.gov.us"
    context.CI_ID = "urn:" + incorrect_domain_name + ":id:ci:001.001.00001"
    print ("    *** The invalid CI ID is: " + context.CI_ID + " \n")


@when('a request is made for the collection instrument using the ID with the incorrect domain name')
def step_impl(context):
    CIendpoint = "/collectioninstrument/id/"
    CIurl = context.CIdomain + context.CIport + CIendpoint + context.CI_ID
    print("    *** The URL to go to is:" + CIurl + " \n")
    context.response = requests.get(CIurl)

    assert context.response.status_code == 400
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('information is returned saying the ID with the incorrect domain name is invalid')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'Invalid ID supplied'


# **********************************************************************************************************************
# Scenario: Collection Instrument ID number value is incorrect
# **********************************************************************************************************************
@given('a collection instrument ID with an incorrect number')
def step_impl(context):
    incorrect_number = "000000"
    context.CI_ID = "urn:ons.gov.uk:id:ci:" + incorrect_number
    print ("    *** The invalid CI ID is: " + context.CI_ID + " \n")


@when('a request is made for the collection instrument using the ID with the incorrect number')
def step_impl(context):
    CIendpoint = "/collectioninstrument/id/"
    CIurl = context.CIdomain + context.CIport + CIendpoint + context.CI_ID
    print("    *** The URL to go to is:" + CIurl + " \n")
    context.response = requests.get(CIurl)

    assert context.response.status_code == 400
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('information is returned saying the ID with the incorrect number is invalid')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'Invalid ID supplied'


# **********************************************************************************************************************
# Scenario: Collection Instrument ID type name is incorrect
# **********************************************************************************************************************
@given('a collection instrument ID with an incorrect type name')
def step_impl(context):
    incorrect_type_name = "XX"
    context.CI_ID = "urn:ons.gov.uk:id:" + incorrect_type_name + ":001.001.00001"
    print ("    *** The invalid CI ID is: " + context.CI_ID + " \n")


@when('a request is made for the collection instrument using the ID with the incorrect type name')
def step_impl(context):
    CIendpoint = "/collectioninstrument/id/"
    CIurl = context.CIdomain + context.CIport + CIendpoint + context.CI_ID
    print("    *** The URL to go to is:" + CIurl + " \n")
    context.response = requests.get(CIurl)

    assert context.response.status_code == 400
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('information is returned saying the ID with the incorrect type name is invalid')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'Invalid ID supplied'





# **********************************************************************************************************************
# Scenario: Collection Instrument is not found
# **********************************************************************************************************************
@given('a collection instrument ID that does not exist')
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


@when('a request is made for the collection instrument data using its ID which does not exist')
def step_impl(context):
    CIendpoint = "/collectioninstrument/id/"
    CIurl = context.CIdomain + context.CIport + CIendpoint + context.collection_instrument_id
    print("    *** The URL to go to is:" + CIurl + " \n")
    context.response = requests.get(CIurl)

    assert context.response.status_code == 404
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('information is returned saying the collection instrument is not found')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'Collection instrument not found'





# **********************************************************************************************************************
# Scenario: Create a new collection instrument
# **********************************************************************************************************************
@given('a new collection instrument')
def step_impl(context):
    context.new_CI = {
        "reference": "test-collection-instrument",
        "surveyId": "urn:ons.gov.uk:id:survey:999.001.00001",
        "id": "urn:ons.gov.uk:id:ci:999.001.00001",
        "ciType": "OFFLINE",
        "classifiers": {
            "RU_REF": "01234567890"
        }
    }


@when('a request is made to create the collection instrument')
def step_impl(context):
    CIendpoint = "/collectioninstrument/"
    CIurl = context.CIdomain + context.CIport + CIendpoint
    print("    *** The URL to go to is: " + CIurl + "\n")
    headers = {'Content-type': 'application/json'}
    context.response = requests.post(CIurl, json=context.new_CI, headers=headers)

    assert context.response.status_code == 201
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('the collection instrument is created successfully')
def step_impl(context):
    pass