"""
This steps file holds common steps used for testing of GET / POST / PUT etc. end points.

Most of the context variables in this file are set up in environment.py.
"""
# TODO: Check content-type assertions. Should these all be in the format of 'application/vnd.ons.<type>'?

from behave import given, then
from psycopg2.extensions import AsIs


# ----------------------------------------------------------------------------------------------------------------------
# Common 'given' steps
# ----------------------------------------------------------------------------------------------------------------------
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


# ----------------------------------------------------------------------------------------------------------------------
# Common 'then' steps
# ----------------------------------------------------------------------------------------------------------------------
@then('the response status code is {status_code}')
def step_impl(context, status_code):
    assert context.response.status_code == int(status_code)


@then('the response returns an ETag')
def step_impl(context):
    assert len(context.response.headers['ETag']) > 0  # TODO: Improve this assertion?


@then('information is returned saying "{text}"')
def step_impl(context, text):
    print("Expected text is: " + text)
    assert context.response.text == text
    assert context.response.headers['Content-Type'] == 'text/html; charset=utf-8'
