import psycopg2


def before_all(context):
    context.CIdomain = "http://127.0.0.1:"
    # context.CIport = "8070"
    context.CIport = "5052"

    # TODO: Associate db stuff only with steps that need it
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
