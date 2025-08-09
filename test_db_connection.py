import dotenv.variables
import psycopg2
import os
import dotenv

Env_Var = dotenv.dotenv_values()

DB_NAME = Env_Var['DB_NAME']
DB_USER = Env_Var['DB_USER']
DB_PASS = Env_Var['DB_PASS']
DB_HOST = Env_Var['DB_HOST']
DB_PORT = Env_Var['DB_PORT']

conn = None
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )

    print("Database connection successful!")

    cur = conn.cursor()

    print("\n--- Fetching all tasks: ---")

    cur.execute("SELECT * FROM tasks;")

    all_tasks = cur.fetchall()

    for task in all_tasks:
        print(
            f"ID: {task[0]}, Title: {task[1]}, Description: {task[2]}, Is Completed: {task[3]}")
    cur.close()

except psycopg2.Error as e:
    print("\nError: Could not connect to the database")
    print(e)
finally:

    if conn:
        conn.close()
        print("\nDatabase connection close.")
