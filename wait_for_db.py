import time
import os
import psycopg2

def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(
                dbname=os.environ['POSTGRES_DB'],
                user=os.environ['POSTGRES_USER'],
                password=os.environ['POSTGRES_PASSWORD'],
                host='db',
                port='5432'
            )
            conn.close()
            break
        except Exception as e:
            print("Waiting for database...")
            time.sleep(5)

if __name__ == "__main__":
    wait_for_db()
