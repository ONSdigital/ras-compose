"""
Most of the context variables in this file are set up in environment.py.
"""
# TODO: Check content-type assertions. Should these all be in the format of 'application/vnd.ons.<type>'?


from psycopg2 import IntegrityError
import ast
import jsonschema
import requests
from psycopg2.extensions import AsIs
from behave import given, then, when

# ----------------------------------------------------------------------------------------------------------------------
# 'given' steps
# ----------------------------------------------------------------------------------------------------------------------
@given('a valid {identifier_type}')
def step_impl(context, identifier_type):
    sql_body = """
        SELECT %s
        FROM ras_collection_instrument.ras_collection_instruments
        LIMIT 1;
    """
    col = AsIs(context.db_table_column)
    context.cursor.execute(sql_body, (col,))
    context.content_row = context.cursor.fetchone()

    if isinstance(context.content_row[0], str):
        context.identifier = context.content_row[0]
    else:
        context.identifier = str(context.content_row[0][context.db_row_content_key])


@given('a new collection instrument has been created')
def step_impl(context):
    import os.path
    assert os.path.exists('features/resources/insert_collection_instrument.sql')

    # TODO: Instead of wrapping this in try/except, could we just rollback in environment.py if error was encountered?
    try:
        context.cursor.execute(open("features/resources/insert_collection_instrument.sql", "r").read())
        context.connection.commit()
    except IntegrityError:
        print("INFO: Record already exists in db. Possibly caused by a previous step failing and connection not rolling back.")
        context.connection.rollback()
        return
    assert context.cursor.rowcount > 0


@given('a {identifier_type} of "{identifier}"')
def step_impl(context, identifier_type, identifier):
    context.identifier = identifier


@given('one or more collection instruments exist')
def step_impl(context):
    sql_body = """
        SELECT EXISTS (
            SELECT *
            FROM ras_collection_instrument.ras_collection_instruments
        )
    """
    context.cursor.execute(sql_body,)
    identifier_exists = context.cursor.fetchone()[0]
    assert identifier_exists is True


# ----------------------------------------------------------------------------------------------------------------------
# 'when' steps
# ----------------------------------------------------------------------------------------------------------------------
@when('a request is made for the collection instrument data')
def step_impl(context):
    ci_endpoint = "/collectioninstrument" + context.endpoint_parameter
    url = context.ci_domain + context.ci_port + ci_endpoint + context.identifier
    context.response = requests.get(url, headers=context.valid_authorisation_header)
    print(url)


#TODO: This is very similar to "a request is made for the collection instrument data".
@when('a request is made for one or more collection instrument data')
def step_impl(context):
    ci_endpoint = "/collectioninstrument"
    url = context.ci_domain + context.ci_port + ci_endpoint
    context.response = requests.get(url, headers=context.valid_authorisation_header)
    print(url)


@when('the new collection instrument has been removed')
def step_impl(context):
    delete_body = """
        DELETE FROM ras_collection_instrument.ras_collection_instruments
        WHERE %s = %s;
        """
    col = AsIs(context.db_table_column)
    context.cursor.execute(delete_body, (col, context.identifier))
    context.connection.commit() if context.cursor.rowcount == 1 else context.connection.rollback()
    assert context.cursor.rowcount == 1


# ----------------------------------------------------------------------------------------------------------------------
# 'then' steps
# ----------------------------------------------------------------------------------------------------------------------
@then('check the returned data are correct')
def step_impl(context):
    assert context.response.headers['Content-Type'] == 'collection+json'
    context.response_text = ast.literal_eval(context.response.text)

    if isinstance(context.response_text, list):
        for row in context.response_text:
            jsonschema.validate(row, context.schema_definition)
    else:
        jsonschema.validate(context.response_text, context.schema_definition)
