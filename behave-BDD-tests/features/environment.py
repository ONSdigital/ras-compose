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


def after_scenario(context, scenario):
    if 'connect_to_database' in scenario.tags:
        context.connection.close()
