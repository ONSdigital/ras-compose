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
/>  behave --tags=-wip      ('--tags=-wip' will skip any scenarios marked with @wip)
"""


# TODO: Lots of repetition inside then/when steps for GET - can these be moved to a common function or something similar?

# TODO: Modularise into separate scripts!

# TODO: Only using a basic implementation of (jsonschema) validate. Could we validate on things like missing key, value length etc?

# TODO: Dynamically created collection instruments used in some tests are dependent on schema data being available in db. Is this
#       the best way to test, or do things need to be hard-coded instead?

# TODO: Do POST requests need to remove any rows created in schema after a scenario?


from ast import literal_eval
import requests
from behave import given, when, then
from jsonschema import validate
# from sqlalchemy import exc


# ----------------------------------------------------------------------------------------------------------------------
# Scenario: CI Status Running
# ----------------------------------------------------------------------------------------------------------------------
@given('The CI status is active')
def step_impl(context):
    ci_endpoint = "/status"
    CIurl = context.ci_domain + context.ci_port + ci_endpoint
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




# ----------------------------------------------------------------------------------------------------------------------
#
# GET - Collection Instrument ID URN Tests
#
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Obtain Collection Instrument data by ID
# ----------------------------------------------------------------------------------------------------------------------
@given('a valid collection instrument ID')
def step_impl(context):
   context.cursor.execute(
       "SELECT urn "
       "FROM ras_collection_instrument.ras_collection_instruments "
       "LIMIT 1"
   )
   content_row = context.cursor.fetchone()
   context.id_urn = content_row[0]


@when('a request is made for the collection instrument data by ID')
def step_impl(context):
    ci_endpoint = "/collectioninstrument/id/"

    url = context.ci_domain + context.ci_port + ci_endpoint + context.id_urn
    print("    *** The URL to go to is: " + url + " \n")
    context.response = requests.get(url)

    assert context.response.status_code == 200
    assert context.response.headers['Content-Type'] == 'collection+json'


@then('check the returned data by collection instrument ID is correct')
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
    response_text = literal_eval(context.response.text)
    response_json = response_text[0]
    validate(response_json, schema_definition)


# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Collection Instrument ID domain name is incorrect
# ----------------------------------------------------------------------------------------------------------------------
@given('a collection instrument ID with an incorrect domain name')
def step_impl(context):
    incorrect_domain_name = "ons.gov.us"
    context.id_urn = "urn:" + incorrect_domain_name + ":id:ci:001.001.00001"
    print ("    *** The invalid CI ID is: " + context.id_urn + " \n")


@when('a request is made for the collection instrument using the ID with the incorrect domain name')
def step_impl(context):
    ci_endpoint = "/collectioninstrument/id/"
    CIurl = context.ci_domain + context.ci_port + ci_endpoint + context.id_urn
    print("    *** The URL to go to is:" + CIurl + " \n")
    context.response = requests.get(CIurl)

    assert context.response.status_code == 400
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('information is returned saying the ID with the incorrect domain name is invalid')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'Invalid ID supplied'


# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Collection Instrument ID number value is incorrect
# ----------------------------------------------------------------------------------------------------------------------
@given('a collection instrument ID with an incorrect number')
def step_impl(context):
    incorrect_number = "000000"
    context.id_urn = "urn:ons.gov.uk:id:ci:" + incorrect_number
    print ("    *** The invalid CI ID is: " + context.id_urn + " \n")


@when('a request is made for the collection instrument using the ID with the incorrect number')
def step_impl(context):
    ci_endpoint = "/collectioninstrument/id/"
    CIurl = context.ci_domain + context.ci_port + ci_endpoint + context.id_urn
    print("    *** The URL to go to is:" + CIurl + " \n")
    context.response = requests.get(CIurl)

    assert context.response.status_code == 400
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('information is returned saying the ID with the incorrect number is invalid')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'Invalid ID supplied'


# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Collection Instrument ID type name is incorrect
# ----------------------------------------------------------------------------------------------------------------------
@given('a collection instrument ID with an incorrect type name')
def step_impl(context):
    incorrect_type_name = "XX"
    context.id_urn = "urn:ons.gov.uk:id:" + incorrect_type_name + ":001.001.00001"
    print ("    *** The invalid CI ID is: " + context.id_urn + " \n")


@when('a request is made for the collection instrument using the ID with the incorrect type name')
def step_impl(context):
    ci_endpoint = "/collectioninstrument/id/"
    CIurl = context.ci_domain + context.ci_port + ci_endpoint + context.id_urn
    print("    *** The URL to go to is:" + CIurl + " \n")
    context.response = requests.get(CIurl)

    assert context.response.status_code == 400
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('information is returned saying the ID with the incorrect type name is invalid')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'Invalid ID supplied'


# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Collection Instrument ID with the lowest boundary is not found
# ----------------------------------------------------------------------------------------------------------------------
@given('a collection instrument ID with the lowest boundary that does not exist')
def step_impl(context):
    context.lowest_boundary_id_urn = 'urn:ons.gov.uk:id:ci:000.000.00000'


@when('a request is made for the collection instrument using the ID with the lowest boundary')
def step_impl(context):
    ci_endpoint = "/collectioninstrument/id/"
    CIurl = context.ci_domain + context.ci_port + ci_endpoint + context.lowest_boundary_id_urn
    print("    *** The URL to go to is:" + CIurl + " \n")
    context.response = requests.get(CIurl)

    assert context.response.status_code == 404
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('information is returned saying the ID with the lowest boundary is not found')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'Collection instrument not found'


# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Collection Instrument ID with the highest boundary is not found
# ----------------------------------------------------------------------------------------------------------------------
@given('a collection instrument ID with the highest boundary that does not exist')
def step_impl(context):
    context.highest_boundary_id_urn = 'urn:ons.gov.uk:id:ci:999.999.99999'


@when('a request is made for the collection instrument using the ID with the highest boundary')
def step_impl(context):
    ci_endpoint = "/collectioninstrument/id/"
    CIurl = context.ci_domain + context.ci_port + ci_endpoint + context.highest_boundary_id_urn
    print("    *** The URL to go to is:" + CIurl + " \n")
    context.response = requests.get(CIurl)

    assert context.response.status_code == 404
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('information is returned saying the ID with the highest boundary is not found')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'Collection instrument not found'


# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Collection Instrument ID number value too low
# ----------------------------------------------------------------------------------------------------------------------
@given('a collection instrument ID with a number value too low')
def step_impl(context):
    invalid_low_number = "-1000.-1000.-100000"
    context.id_urn = "urn:ons.gov.uk:id:ci:" + invalid_low_number
    print ("    *** The invalid CI ID is: " + context.id_urn + " \n")


@when('a request is made for the collection instrument using the ID with the number value too low')
def step_impl(context):
    ci_endpoint = "/collectioninstrument/id/"
    CIurl = context.ci_domain + context.ci_port + ci_endpoint + context.id_urn
    print("    *** The URL to go to is:" + CIurl + " \n")
    context.response = requests.get(CIurl)

    assert context.response.status_code == 400
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('information is returned saying the ID with the number value too low is invalid')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'Invalid ID supplied'


# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Collection Instrument ID number value too high
# ----------------------------------------------------------------------------------------------------------------------
@given('a collection instrument ID with a number value too high')
def step_impl(context):
    invalid_high_number = "9999.9999.999999"
    context.id_urn = "urn:ons.gov.uk:id:ci:" + invalid_high_number
    print ("    *** The invalid CI ID is: " + context.id_urn + " \n")


@when('a request is made for the collection instrument using the ID with the number value too high')
def step_impl(context):
    ci_endpoint = "/collectioninstrument/id/"
    CIurl = context.ci_domain + context.ci_port + ci_endpoint + context.id_urn
    print("    *** The URL to go to is:" + CIurl + " \n")
    context.response = requests.get(CIurl)

    assert context.response.status_code == 400
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('information is returned saying the ID with the number value too high is invalid')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'Invalid ID supplied'


# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Collection Instrument ID is not found
# ----------------------------------------------------------------------------------------------------------------------
# @given('a collection instrument ID that does not exist')
# def step_impl(context):
#     context.cursor.execute("SELECT content "
#                   "FROM ras_collection_instruments "
#                   "LIMIT 1")
#     content_row = context.cursor.fetchone()
#     id_section = content_row[0]['id'].split('.')
#
#     # Replace the ID suffix with an invalid number e.g. '99999' (assuming it won't ever be this high!)
#     id_section[-1] = len(id_section[-1]) * '9'
#
#     context.collection_instrument_id = '.'.join(id_section)
#     print('    *** The CI to find is: ' + context.collection_instrument_id)
#
#
# @when('a request is made for the collection instrument data using its ID which does not exist')
# def step_impl(context):
#     ci_endpoint = "/id/"
#     CIurl = context.ci_domain + context.ci_port + ci_endpoint + context.collection_instrument_id
#     print("    *** The URL to go to is:" + CIurl + " \n")
#     context.response = requests.get(CIurl)
#
#     assert context.response.status_code == 404
#     assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'
#
#
# @then('information is returned saying the collection instrument is not found (ID)')
# def step_impl(context):
#     print("    *** Response is: ", context.response.text, "\n")
#     assert context.response.text == 'Collection instrument not found'








# ----------------------------------------------------------------------------------------------------------------------
#
# GET - Collection Instruments Survey ID URN Tests
#
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Obtain Collection Instrument data by survey ID
# ----------------------------------------------------------------------------------------------------------------------
@given('a valid collection instrument survey ID')
def step_impl(context):
   context.cursor.execute(
       "SELECT survey_urn "
       "FROM ras_collection_instrument.ras_collection_instruments "
       "LIMIT 1"
   )
   content_row = context.cursor.fetchone()
   context.survey_urn = content_row[0]


@when('a request is made for the collection instrument data by survey ID')
def step_impl(context):
    ci_endpoint = "/collectioninstrument/surveyid/"

    url = context.ci_domain + context.ci_port + ci_endpoint + context.survey_urn
    print("    *** The URL to go to is: " + url + " \n")
    context.response = requests.get(url)

    assert context.response.status_code == 200
    assert context.response.headers['Content-Type'] == 'collection+json'


@then('check the returned data by collection instrument survey ID is correct')
def step_impl(context):

    schema_definition = {
        "type": "object",
        "properties": {
            "reference": {"type": "string"},
            "id": {"type": "string"},
            "surveyid": {"type": "string"},
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
    response_text = literal_eval(context.response.text)
    response_json = response_text[0]
    validate(response_json, schema_definition)


# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Collection Instrument survey ID domain name is incorrect
# ----------------------------------------------------------------------------------------------------------------------
@given('a collection instrument survey ID with an incorrect domain name')
def step_impl(context):
    incorrect_domain_name = "ons.gov.us"
    context.survey_urn = "urn:" + incorrect_domain_name + ":id:survey:001.001.00001"
    print ("    *** The invalid CI survey ID is: " + context.survey_urn + " \n")


@when('a request is made for the collection instrument using the survey ID with the incorrect domain name')
def step_impl(context):
    ci_endpoint = "/collectioninstrument/surveyid/"
    CIurl = context.ci_domain + context.ci_port + ci_endpoint + context.survey_urn
    print("    *** The URL to go to is:" + CIurl + " \n")
    context.response = requests.get(CIurl)

    assert context.response.status_code == 400  # TODO: Check this assertion is correct
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('information is returned saying the survey ID with the incorrect domain name is invalid')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'Invalid ID supplied'  # TODO: Check this assertion is correct


# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Collection Instrument survey ID number value is incorrect
# ----------------------------------------------------------------------------------------------------------------------
@given('a collection instrument survey ID with an incorrect number')
def step_impl(context):
    incorrect_number = "000000"
    context.survey_urn = "urn:ons.gov.uk:id:survey:" + incorrect_number
    print ("    *** The invalid CI survey ID is: " + context.survey_urn + " \n")


@when('a request is made for the collection instrument using the survey ID with the incorrect number')
def step_impl(context):
    ci_endpoint = "/collectioninstrument/surveyid/"
    CIurl = context.ci_domain + context.ci_port + ci_endpoint + context.survey_urn
    print("    *** The URL to go to is:" + CIurl + " \n")
    context.response = requests.get(CIurl)

    assert context.response.status_code == 400
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('information is returned saying the survey ID with the incorrect number is invalid')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'Invalid ID supplied'


# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Collection Instrument survey ID type name is incorrect
# ----------------------------------------------------------------------------------------------------------------------
@given('a collection instrument survey ID with an incorrect type name')
def step_impl(context):
    incorrect_type_name = "XX"
    context.survey_urn = "urn:ons.gov.uk:id:" + incorrect_type_name + ":001.001.00001"
    print ("    *** The invalid CI survey ID is: " + context.survey_urn + " \n")


@when('a request is made for the collection instrument using the survey ID with the incorrect type name')
def step_impl(context):
    ci_endpoint = "/collectioninstrument/surveyid/"
    CIurl = context.ci_domain + context.ci_port + ci_endpoint + context.survey_urn
    print("    *** The URL to go to is:" + CIurl + " \n")
    context.response = requests.get(CIurl)

    assert context.response.status_code == 400
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('information is returned saying the survey ID with the incorrect type name is invalid')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'Invalid ID supplied'


# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Collection Instrument survey ID with the lowest boundary is not found
# ----------------------------------------------------------------------------------------------------------------------
@given('a collection instrument survey ID with the lowest boundary that does not exist')
def step_impl(context):
    context.lowest_boundary_survey_urn = 'urn:ons.gov.uk:id:survey:000.000.00000'


@when('a request is made for the collection instrument using the survey ID with the lowest boundary')
def step_impl(context):
    ci_endpoint = "/collectioninstrument/surveyid/"
    CIurl = context.ci_domain + context.ci_port + ci_endpoint + context.lowest_boundary_survey_urn
    print("    *** The URL to go to is:" + CIurl + " \n")
    context.response = requests.get(CIurl)

    assert context.response.status_code == 404
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('information is returned saying the survey ID with the lowest boundary is not found')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'Collection instrument not found'  # TODO: Check this assertion is correct


# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Collection Instrument survey ID with the highest boundary is not found
# ----------------------------------------------------------------------------------------------------------------------
@given('a collection instrument survey ID with the highest boundary that does not exist')
def step_impl(context):
    context.highest_boundary_survey_urn = 'urn:ons.gov.uk:id:survey:999.999.99999'


@when('a request is made for the collection instrument using the survey ID with the highest boundary')
def step_impl(context):
    ci_endpoint = "/collectioninstrument/surveyid/"
    CIurl = context.ci_domain + context.ci_port + ci_endpoint + context.highest_boundary_survey_urn
    print("    *** The URL to go to is:" + CIurl + " \n")
    context.response = requests.get(CIurl)

    assert context.response.status_code == 404
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('information is returned saying the survey ID with the highest boundary is not found')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'Collection instrument not found'


# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Collection Instrument survey ID number value too low
# ----------------------------------------------------------------------------------------------------------------------
@given('a collection instrument survey ID with a number value too low')
def step_impl(context):
    invalid_low_number = "-1000.-1000.-100000"
    context.survey_urn = "urn:ons.gov.uk:id:survey:" + invalid_low_number
    print ("    *** The invalid CI survey ID is: " + context.survey_urn + " \n")


@when('a request is made for the collection instrument using the survey ID with the number value too low')
def step_impl(context):
    ci_endpoint = "/collectioninstrument/surveyid/"
    CIurl = context.ci_domain + context.ci_port + ci_endpoint + context.survey_urn
    print("    *** The URL to go to is:" + CIurl + " \n")
    context.response = requests.get(CIurl)

    assert context.response.status_code == 400
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('information is returned saying the survey ID with the number value too low is invalid')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'Invalid ID supplied'


# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Collection Instrument survey ID number value too high
# ----------------------------------------------------------------------------------------------------------------------
@given('a collection instrument survey ID with a number value too high')
def step_impl(context):
    invalid_high_number = "9999.9999.999999"
    context.survey_urn = "urn:ons.gov.uk:id:survey:" + invalid_high_number
    print ("    *** The invalid CI survey ID is: " + context.survey_urn + " \n")


@when('a request is made for the collection instrument using the survey ID with the number value too high')
def step_impl(context):
    ci_endpoint = "/collectioninstrument/surveyid/"
    CIurl = context.ci_domain + context.ci_port + ci_endpoint + context.survey_urn
    print("    *** The URL to go to is:" + CIurl + " \n")
    context.response = requests.get(CIurl)

    assert context.response.status_code == 400
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('information is returned saying the survey ID with the number value too high is invalid')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'Invalid ID supplied'


# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Collection Instrument survey ID is not found
# ----------------------------------------------------------------------------------------------------------------------
# @given('a collection instrument survey ID that does not exist')
# def step_impl(context):
#     context.cursor.execute("SELECT content "
#                   "FROM ras_collection_instruments "
#                   "LIMIT 1")
#     content_row = context.cursor.fetchone()
#     id_section = content_row[0]['id'].split('.')
#
#     # Replace the survey ID suffix with an invalid number e.g. '99999' (assuming it won't ever be this high!)
#     id_section[-1] = len(id_section[-1]) * '9'
#
#     context.collection_instrument_id = '.'.join(id_section)
#     print('    *** The CI to find is: ' + context.collection_instrument_id)
#
#
# @when('a request is made for the collection instrument data using its survey ID which does not exist')
# def step_impl(context):
#     ci_endpoint = "/surveyid/"
#     CIurl = context.ci_domain + context.ci_port + ci_endpoint + context.collection_instrument_id
#     print("    *** The URL to go to is:" + CIurl + " \n")
#     context.response = requests.get(CIurl)
#
#     assert context.response.status_code == 404
#     assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'
#
#
# @then('information is returned saying the collection instrument is not found (survey ID)')
# def step_impl(context):
#     print("    *** Response is: ", context.response.text, "\n")
#     assert context.response.text == 'Collection instrument not found'




















# ----------------------------------------------------------------------------------------------------------------------
#
# POST - Create collection instrument
#
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Create a new collection instrument
# ----------------------------------------------------------------------------------------------------------------------
@given('a new collection instrument')
def step_impl(context):
    context.new_ci = {
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
    ci_endpoint = "/collectioninstrument/"
    CIurl = context.ci_domain + context.ci_port + ci_endpoint
    print("    *** The URL to go to is: " + CIurl + "\n")
    headers = {'Content-type': 'application/json'}
    context.response = requests.post(CIurl, json=context.new_ci, headers=headers)

    assert context.response.status_code == 201
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('the collection instrument is created successfully')
def step_impl(context):
    pass