from typing import List, Optional
from fastapi import FastAPI
import psycopg2
import dotenv
from pydantic import BaseModel
from fastapi import HTTPException, status

app = FastAPI()

Env_Var = dotenv.dotenv_values()

DB_NAME = Env_Var['DB_NAME']
DB_USER = Env_Var['DB_USER']
DB_PASS = Env_Var['DB_PASS']
DB_HOST = Env_Var['DB_HOST']
DB_PORT = Env_Var['DB_PORT']


@app.get("/")
async def read_root():
    return {"message": "Hello Fucking World"}


def get_db_conn():
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

        return conn

    except psycopg2.Error as e:
        print("\nError: Could not connect to the database")
        print(e)


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    is_completed: bool = False

    class Config:
        orm_mode = True
        from_attributes = True


@app.get("/tasks", response_model=List[Task])
async def read_tasks():

    conn = None
    cur = None
    tasks = []

    try:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, title, description, is_completed FROM tasks;")

        rows = cur.fetchall()

        for row in rows:
            task_dict = {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "is_completed": row[3]
            }
            tasks.append(Task(**task_dict))

    except psycopg2.Error as e:
        print(f"Database error{e}")
        raise e

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
async def read_single_task(task_id: int):
    try:
        conn = get_db_conn()
        cur = conn.cursor()

        cur.execute(
            "SELECT id, title, description, is_completed FROM tasks WHERE id = %s", (task_id,))  

        task = cur.fetchone()

        if task is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found.")

    except psycopg2.Error as e:
        print(f"Database error{e}")
        raise e

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

    return Task(id=task[0], title=task[1], description=task[2], is_completed=task[3])
