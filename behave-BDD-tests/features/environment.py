import psycopg2  # TODO: Should we be using SQLAlchemy instead?


def before_all(context):
    context.ci_domain = "http://127.0.0.1:"
    # context.ci_port = "8070"
    context.ci_port = "5052"

    # TODO: db cursor is created for each scenario at the moment! Should only trigger for steps that need it (behave tags?)
    context.connection = psycopg2.connect(
        dbname='postgres',
        user='ras_collection_instrument',
        password='password',
        host='127.0.0.1',
        port='5431'
    )
    context.cursor = context.connection.cursor()


def after_all(context):
    context.connection.close()
