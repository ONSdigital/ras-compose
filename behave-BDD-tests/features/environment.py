import psycopg2


def before_feature(context, feature):
    context.ci_domain = "http://127.0.0.1:"
    context.ci_port = "5052"

    context.schema_definition = {
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


def before_scenario(context, scenario):
    if 'connect_to_database' in scenario.tags:
        context.connection = psycopg2.connect(
            dbname='postgres',
            user='ras_collection_instrument',
            password='password',
            host='127.0.0.1',
            port='5431'
        )
        context.cursor = context.connection.cursor()

    steps_list = [step.name for step in scenario.steps]
    for step in steps_list:
        if 'Collection Instrument ID' in step:
            context.db_table_column = 'urn'
            context.endpoint_parameter = '/id/'
            context.urn_id = 'ci'
            break
        elif 'Survey ID' in step:
            context.db_table_column = 'survey_urn'
            context.endpoint_parameter = '/surveyid/'
            context.urn_id = 'surveyid'
            break
        elif 'Reference' in step:
            context.db_table_column = 'content'
            context.db_row_content_key = 'reference'
            context.endpoint_parameter = '/reference/'
            break
        elif 'Classifier' in step:
            context.db_table_column = 'content'
            context.db_row_content_key = 'classifiers'
            context.endpoint_parameter = '/?classifier='
            break


def after_scenario(context, scenario):
    if 'connect_to_database' in scenario.tags:
        if context.failed:
            context.connection.rollback()
        context.connection.commit()
        context.connection.close()
