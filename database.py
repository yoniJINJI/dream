
import psycopg2

def connect_to_db():
    conn = psycopg2.connect(
        dbname='dream',
        user='postgres',
        password='hvj2uj6d',
        host='database-1.cpikosqu4qoq.us-east-1.rds.amazonaws.com'
    )
    return conn

def fetch_data(query):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result
