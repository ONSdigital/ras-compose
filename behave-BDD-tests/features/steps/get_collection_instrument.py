"""
Most of the context variables in this file are set up in environment.py.
"""
# TODO: Only using a basic implementation of (jsonschema) validate. Could we validate on things like missing key, value length etc?
# TODO: Check content-type assertions. Should these all be in the format of 'application/vnd.ons.<type>'?


from psycopg2 import IntegrityError
import ast
import jsonschema
from psycopg2.extensions import AsIs
import requests
from behave import given, then, when

# ----------------------------------------------------------------------------------------------------------------------
# Common 'given' steps
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
    content_row = context.cursor.fetchone()

    if isinstance(content_row[0], str):
        context.identifier = content_row[0]
    else:
        context.identifier = str(content_row[0][context.db_row_content_key])


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


@given('the {identifier_type} of the new collection instrument')
def step_impl(context, identifier_type):
    sql_body = """
        SELECT %s
        FROM ras_collection_instrument.ras_collection_instruments
        ORDER BY %s DESC
        LIMIT 1;
    """
    col = AsIs(context.db_table_column)
    context.cursor.execute(sql_body, (col, col))
    content_row = context.cursor.fetchone()

    if isinstance(content_row[0], str):
        context.identifier = content_row[0]
    else:
        context.identifier = str(content_row[0][context.db_row_content_key])


@given('a {identifier_type} of "{identifier}"')
def step_impl(context, identifier_type, identifier):
    # Ensure passed in id doesn't already exist?
    # sql_body = """
    #      SELECT EXISTS (
    #          SELECT *
    #          FROM ras_collection_instrument.ras_collection_instruments
    #          WHERE %s = %s
    #          )
    #  """
    # context.cursor.execute(sql_body, (AsIs(context.db_table_column), identifier))
    # identifier_exists = context.cursor.fetchone()[0]
    # assert identifier_exists is False
    context.identifier = identifier


# ----------------------------------------------------------------------------------------------------------------------
# Common 'when' steps
# ----------------------------------------------------------------------------------------------------------------------
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


@when('a request is made for the collection instrument data')
def step_impl(context):
    ci_endpoint = "/collectioninstrument" + context.endpoint_parameter
    url = context.ci_domain + context.ci_port + ci_endpoint + context.identifier
    context.response = requests.get(url)
    print(url)


# ----------------------------------------------------------------------------------------------------------------------
# Common 'then' steps
# ----------------------------------------------------------------------------------------------------------------------
@then('check the returned data are correct')
def step_impl(context):
    assert context.response.headers['Content-Type'] == 'collection+json'
    context.response_text = ast.literal_eval(context.response.text)
    for row in context.response_text:
        jsonschema.validate(row, context.schema_definition)


@then('information is returned saying "{error_text}"')
def step_impl(context, error_text):
    print("Expected text is: " + error_text)
    assert context.response.text == error_text
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'


@then('the response status code is {status_code}')
def step_impl(context, status_code):
    assert context.response.status_code == int(status_code)


@then('the response returns an e-tag')
def step_impl(context):
    assert len(context.response.headers['ETag']) > 0  # TODO: Improve this assertion?
