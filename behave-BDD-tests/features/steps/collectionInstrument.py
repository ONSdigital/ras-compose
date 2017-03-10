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

# TODO: Modularise into separate scripts!

# TODO: Lots of repetition inside then/when steps for GET - can these be moved to a common function or something similar?

# TODO: Only using a basic implementation of (jsonschema) validate. Could we validate on things like missing key, value length etc?

# TODO: Dynamically created collection instruments used in some tests are dependent on schema data being available in db. Is this
#       the best way to test, or do things need to be hard-coded instead?

# TODO: Do POST requests need to remove any rows created in schema after a scenario?

# TODO: For SQL cursor execution, handle transactions inside 'with' statements (check if environment.py can be changed to aid this)

# TODO: Check content-type assertions. Should these all be in the format of 'application/vnd.ons.<type>'?


from ast import literal_eval
from requests import get, post, put, options
from behave import given, when, then
from jsonschema import validate


# ----------------------------------------------------------------------------------------------------------------------
# Scenario: CI Status Running
# ----------------------------------------------------------------------------------------------------------------------
# @given('The CI status is active')
# def step_impl(context):
#     ci_endpoint = "/status"
#     ci_url = context.ci_domain + context.ci_port + ci_endpoint
#     print ("    *** The URL to go to is:" + ci_url + " \n")
#     context.response = requests.get(ci_url)
#
#
# @when('A request for status is given')
# def step_impl(context):
#     print ("    *** HTTP Response code is:", context.response.status_code, " \n\n")
#     assert context.response.status_code == 200
#
#
# @then('The CI micro service returns status information about itself')
# def step_impl(context):
#     print ("    *** Response is: ", context.response.text, "\n")
#     assert context.response.text == "Collection Instrument service is running"
#




# ----------------------------------------------------------------------------------------------------------------------
#
# GET - Collection Instrument Tests (one or more)
#
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Obtain data for one or more Collection Instruments
# ----------------------------------------------------------------------------------------------------------------------
@given('one or more collection instruments exist')
def step_impl(context):
    context.cursor.execute("""
       SELECT *
       FROM ras_collection_instrument.ras_collection_instruments
       LIMIT 1
    """)
    assert context.cursor.rowcount > 0


@when('a request is made for data for one or more collection instruments')
def step_impl(context):
    ci_endpoint = "/collectioninstrument"

    url = context.ci_domain + context.ci_port + ci_endpoint
    print("    *** The URL to go to is: " + url + " \n")
    context.response = get(url)

    context.response_text = literal_eval(context.response.text)

    assert context.response.status_code == 200
    assert context.response.headers['Content-Type'] == 'collection+json'
    assert len(context.response_text) > 0


@then('check the returned data for one or more collection instruments are correct')
def step_impl(context):
    for row in context.response_text:
        validate(row, context.schema_definition)




# ----------------------------------------------------------------------------------------------------------------------
#
# GET - Collection Instrument query by classifier
#
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Obtain Collection Instrument data by classifier
# ----------------------------------------------------------------------------------------------------------------------
@given('a valid collection instrument classifier')
def step_impl(context):
   context.cursor.execute(
       "SELECT content "
       "FROM ras_collection_instrument.ras_collection_instruments "
       "LIMIT 1"
   )
   content_row = context.cursor.fetchone()
   assert context.cursor.rowcount == 1
   context.classifier = str(content_row[0]['classifiers'])


@when('a request is made for the collection instrument data by classifier')
def step_impl(context):
    ci_endpoint = "/collectioninstrument/"
    classifier_query = "?classifier=" + context.classifier

    url = context.ci_domain + context.ci_port + ci_endpoint + classifier_query
    print("    *** The URL to go to is: " + url + " \n")
    context.response = get(url)

    assert context.response.status_code == 200
    assert context.response.headers['Content-Type'] == 'collection+json'

    context.response_text = literal_eval(context.response.text)


@then('check the returned data by collection instrument classifier are correct')
def step_impl(context):
    for row in context.response_text:
        validate(row, context.schema_definition)


# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Collection Instrument classifier is unknown
# ----------------------------------------------------------------------------------------------------------------------
@given('an unknown collection instrument classifier name')
def step_impl(context):
    context.unknown_classifier_name = "{'TEST_UNKNOWN_CLASSIFIER_NAME':'ABC'}"
    print ("    *** The unknown classifier is: " + context.unknown_classifier_name + "\n")


@when('a request is made for the collection instrument using the unknown classifier name')
def step_impl(context):
    ci_endpoint = "/collectioninstrument/"
    classifier_query = "?classifier=" + context.unknown_classifier_name

    url = context.ci_domain + context.ci_port + ci_endpoint + classifier_query
    print("    *** The URL to go to is:" + url + " \n")
    context.response = get(url)

    assert context.response.status_code == 400  # TODO: Check this assertion is correct
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'  # TODO: Check this assertion is correct


@then('information is returned saying the collection instrument is not found using the unknown classifier name')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'bad input parameter'  # TODO: Check this assertion is correct


# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Collection Instrument classifier query without enclosing braces
# ----------------------------------------------------------------------------------------------------------------------
@given('a collection instrument classifier query without enclosing braces')
def step_impl(context):
    context.malformed_classifier = "'TEST_MALFORMED_CLASSIFIER':'ABC'"
    print ("    *** The classifier without enclosing braces is: " + context.malformed_classifier + "\n")


@when('a request is made for the collection instrument using the classifier without enclosed braces')
def step_impl(context):
    ci_endpoint = "/collectioninstrument/"
    classifier_query = "?classifier=" + context.malformed_classifier

    url = context.ci_domain + context.ci_port + ci_endpoint + classifier_query
    print("    *** The URL to go to is:" + url + " \n")
    context.response = get(url)

    assert context.response.status_code == 400
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('information is returned saying the classifier without enclosed braces is invalid')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'bad input parameter'


# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Collection Instrument classifier query using an incorrect query type
# ----------------------------------------------------------------------------------------------------------------------
@given('a collection instrument query using an incorrect query type')
def step_impl(context):
    context.incorrect_query_type = "?incorrect={'CLASSIFIER':'A'}"
    print ("    *** The incorrect query is: " + context.incorrect_query_type + "\n")


@when('a request is made for the collection instrument classifier using the incorrect query type')
def step_impl(context):
    ci_endpoint = "/collectioninstrument/"

    url = context.ci_domain + context.ci_port + ci_endpoint + context.incorrect_query_type
    print("    *** The URL to go to is:" + url + " \n")
    context.response = get(url)

    assert context.response.status_code == 400
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('information is returned saying the classifier using the incorrect query type is invalid')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'bad input parameter'





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
   assert context.cursor.rowcount > 0


@when('a request is made for the collection instrument data by ID')
def step_impl(context):
    ci_endpoint = "/collectioninstrument/id/"

    url = context.ci_domain + context.ci_port + ci_endpoint + context.id_urn
    print("    *** The URL to go to is: " + url + " \n")
    context.response = get(url)

    assert context.response.status_code == 200
    assert context.response.headers['Content-Type'] == 'collection+json'


@then('check the returned data by collection instrument ID is correct')
def step_impl(context):
    response_text = literal_eval(context.response.text)
    response_json = response_text[0]
    validate(response_json, context.schema_definition)


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
    url = context.ci_domain + context.ci_port + ci_endpoint + context.id_urn
    print("    *** The URL to go to is:" + url + " \n")
    context.response = get(url)

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
    url = context.ci_domain + context.ci_port + ci_endpoint + context.id_urn
    print("    *** The URL to go to is:" + url + " \n")
    context.response = get(url)

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
    url = context.ci_domain + context.ci_port + ci_endpoint + context.id_urn
    print("    *** The URL to go to is:" + url + " \n")
    context.response = get(url)

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
    url = context.ci_domain + context.ci_port + ci_endpoint + context.lowest_boundary_id_urn
    print("    *** The URL to go to is:" + url + " \n")
    context.response = get(url)

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
    url = context.ci_domain + context.ci_port + ci_endpoint + context.highest_boundary_id_urn
    print("    *** The URL to go to is:" + url + " \n")
    context.response = get(url)

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
    url = context.ci_domain + context.ci_port + ci_endpoint + context.id_urn
    print("    *** The URL to go to is:" + url + " \n")
    context.response = get(url)

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
    url = context.ci_domain + context.ci_port + ci_endpoint + context.id_urn
    print("    *** The URL to go to is:" + url + " \n")
    context.response = get(url)

    assert context.response.status_code == 400
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('information is returned saying the ID with the number value too high is invalid')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'Invalid ID supplied'


# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Collection Instrument ID is not found
# ----------------------------------------------------------------------------------------------------------------------
@given('a collection instrument ID that does not exist')
def step_impl(context):
    context.cursor.execute("SELECT urn "
                  "FROM ras_collection_instruments "
                  "LIMIT 1")
    content_row = context.cursor.fetchone()
    id_section = content_row[0].split('.')

    # Replace the ID suffix with an invalid number e.g. '99999' (assuming it won't ever be this high!)
    id_section[-1] = len(id_section[-1]) * '9'

    context.id_urn = '.'.join(id_section)
    print('    *** The CI to find is: ' + context.id_urn)


@when('a request is made for the collection instrument data using its ID which does not exist')
def step_impl(context):
    ci_endpoint = "/collectioninstrument/id/"
    url = context.ci_domain + context.ci_port + ci_endpoint + context.id_urn
    print("    *** The URL to go to is:" + url + " \n")
    context.response = get(url)

    assert context.response.status_code == 404
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('information is returned saying the collection instrument is not found (ID)')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'Collection instrument not found'


# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Add new Collection Instrument for obtaining data by ID
# ----------------------------------------------------------------------------------------------------------------------
@given('a newly created collection instrument for obtaining data by ID')
def step_impl(context):
    #TODO: This 'with' statement doesn't look quite right. Move to environment.py?
    with context.connection:
        context.cursor.execute(open("features/resources/insert_collection_instrument.sql", "r").read())
        context.connection.commit()
    assert context.cursor.rowcount > 0


@when('a request is made for the newly created collection instrument data by ID')
def step_impl(context):
    context.cursor.execute("""
        SELECT urn
        FROM ras_collection_instrument.ras_collection_instruments
        ORDER BY id DESC
        LIMIT 1
    """)
    content_row = context.cursor.fetchone()
    context.id_urn = content_row[0]
    assert context.cursor.rowcount == 1

    ci_endpoint = "/collectioninstrument/id/"
    url = context.ci_domain + context.ci_port + ci_endpoint + context.id_urn
    print("    *** The URL to go to is:" + url + " \n")
    context.response = get(url)

    assert context.response.status_code == 200
    assert context.response.headers['Content-Type'] == 'collection+json'


@then('check the returned data by collection instrument ID are correct')
def step_impl(context):
    response_text = literal_eval(context.response.text)
    response_json = response_text[0]
    validate(response_json, context.schema_definition)


# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Remove new Collection Instrument to ensure its data cannot be obtained
# ----------------------------------------------------------------------------------------------------------------------
@given('a newly created collection instrument for obtaining data by ID has been removed')
def step_impl(context):
    # Get URN for most recently inserted collection instrument
    context.cursor.execute("""
        SELECT urn
        FROM ras_collection_instrument.ras_collection_instruments
        ORDER BY id DESC
        LIMIT 1
    """)
    content_row = context.cursor.fetchone()
    context.id_urn = content_row[0]
    assert context.cursor.rowcount == 1

    # Now remove the row
    delete_body = """
        DELETE FROM ras_collection_instrument.ras_collection_instruments
        WHERE urn = %s;
        """
    context.cursor.execute(delete_body, (context.id_urn,))

    context.connection.commit() if context.cursor.rowcount == 1 else context.connection.rollback()
    assert context.cursor.rowcount == 1


@when('a request is made for the removed collection instrument data by ID')
def step_impl(context):
    ci_endpoint = "/collectioninstrument/id/"
    url = context.ci_domain + context.ci_port + ci_endpoint + context.id_urn
    print("    *** The URL to go to is:" + url + " \n")
    context.response = get(url)

    assert context.response.status_code == 404
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('information is returned saying the removed collection instrument is not found (ID)')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'Collection instrument not found'




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
    context.response = get(url)

    assert context.response.status_code == 200
    assert context.response.headers['Content-Type'] == 'collection+json'

    context.response_text = literal_eval(context.response.text)


@then('check the returned data by collection instrument survey ID are correct')
def step_impl(context):
    for row in context.response_text:
        validate(row, context.schema_definition)


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
    url = context.ci_domain + context.ci_port + ci_endpoint + context.survey_urn
    print("    *** The URL to go to is:" + url + " \n")
    context.response = get(url)

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
    url = context.ci_domain + context.ci_port + ci_endpoint + context.survey_urn
    print("    *** The URL to go to is:" + url + " \n")
    context.response = get(url)

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
    url = context.ci_domain + context.ci_port + ci_endpoint + context.survey_urn
    print("    *** The URL to go to is:" + url + " \n")
    context.response = get(url)

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
    url = context.ci_domain + context.ci_port + ci_endpoint + context.lowest_boundary_survey_urn
    print("    *** The URL to go to is:" + url + " \n")
    context.response = get(url)

    assert context.response.status_code == 404
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('information is returned saying the survey ID with the lowest boundary is not found')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'Collection instrument(s) not found'  # TODO: Check this assertion is correct


# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Collection Instrument survey ID with the highest boundary is not found
# ----------------------------------------------------------------------------------------------------------------------
@given('a collection instrument survey ID with the highest boundary that does not exist')
def step_impl(context):
    context.highest_boundary_survey_urn = 'urn:ons.gov.uk:id:survey:999.999.99999'


@when('a request is made for the collection instrument using the survey ID with the highest boundary')
def step_impl(context):
    ci_endpoint = "/collectioninstrument/surveyid/"
    url = context.ci_domain + context.ci_port + ci_endpoint + context.highest_boundary_survey_urn
    print("    *** The URL to go to is:" + url + " \n")
    context.response = get(url)

    assert context.response.status_code == 404
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('information is returned saying the survey ID with the highest boundary is not found')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'Collection instrument(s) not found'


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
    url = context.ci_domain + context.ci_port + ci_endpoint + context.survey_urn
    print("    *** The URL to go to is:" + url + " \n")
    context.response = get(url)

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
    url = context.ci_domain + context.ci_port + ci_endpoint + context.survey_urn
    print("    *** The URL to go to is:" + url + " \n")
    context.response = get(url)

    assert context.response.status_code == 400
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('information is returned saying the survey ID with the number value too high is invalid')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'Invalid ID supplied'




# ----------------------------------------------------------------------------------------------------------------------
#
# GET - Collection Instruments Reference
#
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Obtain Collection Instrument data by reference
# ----------------------------------------------------------------------------------------------------------------------
@given('a valid collection instrument reference')
def step_impl(context):
    context.cursor.execute(
       "SELECT content "
       "FROM ras_collection_instrument.ras_collection_instruments "
       "LIMIT 1"
    )
    content_row = context.cursor.fetchone()
    context.reference = content_row[0]['reference']
    assert context.cursor.rowcount > 0


@when('a request is made for the collection instrument data by reference')
def step_impl(context):
    ci_endpoint = "/collectioninstrument/reference/"

    url = context.ci_domain + context.ci_port + ci_endpoint + context.reference
    print("    *** The URL to go to is: " + url + " \n")
    context.response = get(url)

    context.response_text = literal_eval(context.response.text)

    assert context.response.status_code == 200
    assert context.response.headers['Content-Type'] == 'collection+json'
    assert len(context.response_text) > 0


@then('check the returned data by collection instrument reference are correct')
def step_impl(context):
    for row in context.response_text:
        validate(row, context.schema_definition)


# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Collection Instrument reference name does not exist
# ----------------------------------------------------------------------------------------------------------------------
@given('a collection instrument reference that does not exist')
def step_impl(context):
    context.incorrect_reference_name = "rsi-fuel(BDDTEST)"
    print("    *** The reference which does not exist is: " + context.incorrect_reference_name + " \n")


@when('a request is made for the collection instrument using the reference that does not exist')
def step_impl(context):
    ci_endpoint = "/collectioninstrument/reference/"
    url = context.ci_domain + context.ci_port + ci_endpoint + context.incorrect_reference_name
    print("    *** The URL to go to is:" + url + " \n")
    context.response = get(url)

    assert context.response.status_code == 404
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('information is returned saying the reference does not exist')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'Collection instrument not found'


# ----------------------------------------------------------------------------------------------------------------------
# Scenario: Collection Instrument reference has non-ASCII character
# ----------------------------------------------------------------------------------------------------------------------
@given('a collection instrument reference with a non-ASCII character')
def step_impl(context):
    context.non_ascii_reference_name = "À"
    print("    *** The non-ASCII reference is: " + context.non_ascii_reference_name + " \n")


@when('a request is made for the collection instrument using the reference with the non-ASCII character')
def step_impl(context):
    ci_endpoint = "/collectioninstrument/reference/"
    url = context.ci_domain + context.ci_port + ci_endpoint + context.non_ascii_reference_name
    print("    *** The URL to go to is:" + url + " \n")
    context.response = get(url)

    assert context.response.status_code == 404
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('information is returned saying the reference with the non-ASCII character is invalid')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'Collection instrument not found'





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
        "surveyId": "urn:ons.gov.uk:id:survey:001.234.56789",
        "id": "urn:ons.gov.uk:id:ci:001.234.56789",
        "ciType": "OFFLINE",
        "classifiers": {
            "RU_REF": "1731"
        }
    }


@when('a request is made to create the collection instrument')
def step_impl(context):
    ci_endpoint = "/collectioninstrument/"
    url = context.ci_domain + context.ci_port + ci_endpoint
    print("    *** The URL to go to is: " + url + "\n")
    headers = {'Content-type': 'application/json'}
    context.response = post(url, json=context.new_ci, headers=headers)

    assert context.response.status_code == 201
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'

    assert len(context.response.headers['Location']) > 0  # TODO: Improve this assertion
    assert len(context.response.headers['ETag']) > 0  # TODO: Improve this assertion


@then('the collection instrument is created successfully')
def step_impl(context):
    print("    *** Response is: ", context.response.text, "\n")
    assert context.response.text == 'item created'









#
# @given('a valid collection instrument "{identifier}"')
# def step_impl(context, identifier):
#     if 'Collection Instrument ID' in identifier:
#         column = 'urn'
#         context.endpoint_parameter = '/id/'
#
#     elif 'Survey ID' in identifier:
#         column = 'survey_urn'
#         context.endpoint_parameter = '/surveyid/'
#     else:
#         print("Bad identifier: " + identifier)
#         assert False
#
#     sql_body = """
#         SELECT %s
#         FROM ras_collection_instrument.ras_collection_instruments
#         LIMIT 1;
#     """
#     context.cursor.execute(sql_body, (column,))
#     content_row = context.cursor.fetchone()
#
#     context.id = content_row[0]
#
#
# @when('a request is made for the collection instrument data by "{identifier}"')
# def step_impl(context, identifier):
#     ci_endpoint = "/collectioninstrument" + context.endpoint_parameter
#
#     url = context.ci_domain + context.ci_port + ci_endpoint + context.id
#     print("    *** The URL to go to is: " + url + " \n")
#     context.response = get(url)
#
#     assert context.response.status_code == 200
#     assert context.response.headers['Content-Type'] == 'collection+json'
#
#     context.response_text = literal_eval(context.response.text)
#
#
# @then('check the returned data by "{identifier}" are correct')
# def step_impl(context, identifier):
#     for row in context.response_text:
#         validate(row, context.schema_definition)


# # ----------------------------------------------------------------------------------------------------------------------
# # Scenario: Collection Instrument <identifier> domain name is incorrect
# # ----------------------------------------------------------------------------------------------------------------------
# @given('a collection instrument "{identifier}" with an incorrect domain name')
# def step_impl(context, identifier):
#     incorrect_domain_name = "ons.gov.us"
#
#     if identifier
#     context.urn = "urn:" + incorrect_domain_name + ":id:" + identifier_type + ":001.001.00001"
#
#     if 'ID' in identifier:
#         context.urn = "urn:" + incorrect_domain_name + ":id:ci:001.001.00001"
#     else:
#         context.urn = "urn:" + incorrect_domain_name + ":id:surveyid:001.001.00001"
#     print ("    *** The invalid CI ID is: " + context.id_urn + " \n")
#
#
# @when('a request is made for the collection instrument using the "{identifier}" with the incorrect domain name')
# def step_impl(context, identifier):
#     ci_endpoint = "/collectioninstrument/" + identifier + "/"
#     url = context.ci_domain + context.ci_port + ci_endpoint + context.urn
#     print("    *** The URL to go to is:" + url + " \n")
#     context.response = get(url)
#
#     assert context.response.status_code == 400
#     assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'
#
#
# @then('information is returned saying the "{identifier}" with the incorrect domain name is invalid')
# def step_impl(context):
#     print("    *** Response is: ", context.response.text, "\n")
#     assert context.response.text == 'Invalid ID supplied'