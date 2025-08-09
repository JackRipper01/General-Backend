import psycopg2
import os


def add_new_task_to_db(conn, cur, title, description, is_completed):
    sql_query = "INSERT INTO tasks (title,description,is_completed) VALUES (%s,%s,%s)"
    cur.execute(sql_query, (title, description, is_completed))
    conn.commit()
