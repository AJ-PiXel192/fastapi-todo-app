import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI() #initializes the web application

# fast api builds the UI btw

# Initialize simple SQLite database
def init_db():
    conn = sqlite3.connect("database.db") #open a connection to an sql lite database, since it doesnt belong yet, create one names database.db
    cursor = conn.cursor() #pen to point towards the sql database
    cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT)")
    conn.commit() #save 
    conn.close() #close the database

init_db() #runs the database function 

class Task(BaseModel):
    title: str    #ensures whatever I send has a text title

# 1. Add Data (REST API POST)
@app.post("/tasks/") #It creates an endpoint that listens for HTTP POST requests at the /tasks/ URL path.
def add_task(task: Task):
    conn = sqlite3.connect("database.db") # opens a connection 
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (title) VALUES (?)", (task.title,)) #adds task to sqllite databsse
    conn.commit()
    conn.close()
    return {"message": "Task added successfully!", "task": task.title}

# 2. Retrieve Data (REST API GET)
@app.get("/tasks/")  #listens for get requests 
def get_tasks():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks") #select all rows and columns
    rows = cursor.fetchall() #packs it all, the rows, into a python list
    # the above, since sql data os messy, and python cannot read it
    # it makes a clean python list, then Fast API can convert it into a JSON and send it straight to the UI
    conn.close()
    return {"tasks": rows}