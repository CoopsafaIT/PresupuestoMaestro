from django.db import connection


def execute_sql_query(query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        result = dictfetchall(cursor)
        return {
            'status': 'ok',
            'data': result
        }
    except Exception as e:
        return {
            'status': 'error',
            'data': e.__str__()
        }
    finally:
        cursor.close()


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
