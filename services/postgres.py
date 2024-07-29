# services/postgres.py

import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine
import pandas as pd

host_name = '127.0.0.1'
database_name = "mydb"
user_name = 'rudra'
password_ = '1234'
port_ = 5432

def connection(func):
    def wrapper(*args, **kwargs):
        connection = None
        try:
            connection = psycopg2.connect(
                host=host_name,
                database=database_name,
                user=user_name,
                password=password_,
                port=port_
            )
            result = func(connection, *args, **kwargs)
            return result
        except Exception as error:
            print(f'Error connecting to the database: {error}')
        finally:
            if connection:
                connection.close()
                print("Connection closed.")
    return wrapper

@connection
def create_schemas(connection, schema):
    try:
        cursor = connection.cursor()
        cursor.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(sql.Identifier(schema)))
        connection.commit()
        cursor.close()
    except Exception as error:
        print(f'Error creating schemas: {error}')

@connection
def dump_to_postgresql(connection, df, schema_name, table_name):
    try:
        engine = create_engine('postgresql+psycopg2://', creator=lambda: connection)
        df.to_sql(table_name, engine, schema=schema_name, if_exists='replace', index=False)
    except Exception as e:
        print(f"Error dumping data into {schema_name}.{table_name} table: {e}")

@connection
def get_tables_in_schema(connection, schema_name):
    try:
        cursor = connection.cursor()
        cursor.execute(
            sql.SQL("SELECT table_name FROM information_schema.tables WHERE table_schema = %s;"),
            [schema_name]
        )
        tables = cursor.fetchall()
        cursor.close()
        return [table[0] for table in tables]
    except Exception as error:
        print(f'Error fetching tables in schema {schema_name}: {error}')
        return []

@connection
def delete_table(connection, schema_name, table_name):
    try:
        cursor = connection.cursor()
        cursor.execute(
            sql.SQL("DROP TABLE IF EXISTS {}.{}").format(
                sql.Identifier(schema_name),
                sql.Identifier(table_name)
            )
        )
        connection.commit()
        cursor.close()
    except Exception as error:
        print(f'Error deleting table {schema_name}.{table_name}: {error}')

@connection
def fetch_data_from_pg(connection, schema_name, table_or_view_name):
    try:
        engine = create_engine('postgresql+psycopg2://', creator=lambda: connection)
        query = f'SELECT * FROM {schema_name}.{table_or_view_name}' 
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        print(f"Error fetching data from {schema_name}.{table_or_view_name}: {e}")
        return None
