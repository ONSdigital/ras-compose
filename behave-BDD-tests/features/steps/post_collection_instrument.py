"""
Most of the context variables in this file are set up in environment.py.
"""
# TODO: Check content-type assertions. Should these all be in the format of 'application/vnd.ons.<type>'?

import requests
from behave import given, then, when

# ----------------------------------------------------------------------------------------------------------------------
# 'given' steps
# ----------------------------------------------------------------------------------------------------------------------
@given('a new collection instrument')
def step_impl(context):
    context.new_ci = {
        "reference": "test-post-collection-instrument",
        "surveyId": "urn:ons.gov.uk:id:survey:001.234.56789",
        "id": "urn:ons.gov.uk:id:ci:001.234.56789",
        "ciType": "OFFLINE",
        "classifiers": {
            "RU_REF": "1731"
        }
    }


@given('an incorrectly formed collection instrument')
def step_impl(context):
    context.new_ci = [{
        "test-key": "test"
    }]


@given('a new collection instrument that already exists')
def step_impl(context):
    context.execute_steps('''
        given a new collection instrument
        when a request is made to create the collection instrument
    ''')

# ----------------------------------------------------------------------------------------------------------------------
# 'when' steps
# ----------------------------------------------------------------------------------------------------------------------
@when('a request is made to create the collection instrument')
def step_impl(context):
    ci_endpoint = "/collectioninstrument/"
    url = context.ci_domain + context.ci_port + ci_endpoint
    context.response = requests.post(
        url,
        json=context.new_ci,
        headers=context.valid_authorisation_header)
    print(url)


# ----------------------------------------------------------------------------------------------------------------------
# 'then' steps
# ----------------------------------------------------------------------------------------------------------------------
@then('the collection instrument is created successfully')
def step_impl(context):
    assert context.response.text == 'item created'


@then('the response returns the location for the data')
def step_impl(context):
    assert context.ci_domain + context.ci_port in context.response.headers['Location']  #TODO: Improve this assertion
