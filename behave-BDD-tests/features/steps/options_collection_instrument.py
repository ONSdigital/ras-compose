"""
Most of the context variables in this file are set up in environment.py.
"""
# TODO: Check content-type assertions. Should these all be in the format of 'application/vnd.ons.<type>'?

import ast
from behave import then, when
import requests


# ----------------------------------------------------------------------------------------------------------------------
# 'when' steps
# ----------------------------------------------------------------------------------------------------------------------
#TODO: This function is pretty much repeated in get and post steps files. Move this function into common_steps.py and parameterise?
@when('a request is made for the collection instrument options')
def step_impl(context):
    ci_endpoint = "/collectioninstrument" + context.endpoint_parameter
    url = context.ci_domain + context.ci_port + ci_endpoint + context.identifier
    context.response = requests.options(url, headers=context.valid_authorisation_header)
    print(url)


# ----------------------------------------------------------------------------------------------------------------------
# 'then' steps
# ----------------------------------------------------------------------------------------------------------------------
@then('check the returned options are correct')
def step_impl(context):
    assert context.response.headers['Content-Type'] == 'collection+json'
    response_json = ast.literal_eval(context.response.text)
    assert 'representation options' in response_json
