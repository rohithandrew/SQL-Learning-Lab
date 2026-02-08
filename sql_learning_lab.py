import os
from dotenv import load_dotenv
import mysql.connector
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

load_dotenv()

con = mysql.connector.connect(
    host = os.getenv('DB_HOST'),
    user = os.getenv('DB_USER'),
    password = os.getenv('DB_PASS'),
    database = os.getenv('DB_NAME')
)

app = FastAPI(title="SQL Learning Lab", version="1.0.0")

class UserCredentials(BaseModel):
    username: str
    password: str

class SQLQuery(BaseModel):
    query: str

@app.get("/")
def read_root():
    return {"message": "Welcome to SQL Learning Lab"}

@app.post("/register")
def register_user(user: UserCredentials):
    if check_username(user.username.lower()):
        raise HTTPException(status_code=400, detail="Username already exists!")
    register(user.username.lower(), user.password)
    return {"message": "Registration Successful!"}

@app.post("/login")
def login_user(user: UserCredentials):
    if not check_username(user.username.lower()):
        raise HTTPException(status_code=401, detail="Username does not exist! Please register first.")
    
    if check_login(user.username.lower(), user.password):
        return {"message": "Login Successful!", "username": user.username.lower()}
    else:
        raise HTTPException(status_code=401, detail="Incorrect password!")

@app.post("/execute-sql/{username}")
def execute_sql(username: str, query: SQLQuery):
    blocked_words = ['SHOW DATABASES', 'SHOW SCHEMAS', 'USE ', 'DROP DATABASE', 'CREATE DATABASE']
    if any(word in query.query.upper() for word in blocked_words):
        raise HTTPException(status_code=403, detail="This action is not allowed.")
    
    db_name = username.lower() + "_db"
    db_init(db_name)

    try:
        res = con.cursor()
        res.execute(query.query)
        result = res.fetchall()
        con.commit()
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error executing query: {str(e)}")

def register(username, password):
    res = con.cursor()
    sql = "insert into login_credentials (username, password) values (%s, %s)"
    user = (username , password)
    res.execute(sql, user)
    con.commit()
    print("Registration Successful!")

def check_login(username, password):
    res = con.cursor()
    sql = "select * from login_credentials where username = %s and password = %s"
    user = (username , password)
    res.execute(sql, user)
    result = res.fetchone()
    
    if result:
        return True
    else:
        return False

def check_username(username):
    res = con.cursor()
    sql = "select * from login_credentials where username = %s"
    user = (username ,)
    res.execute(sql, user)
    result = res.fetchone()

    if result:
        return True
    else:
        return False
    
def db_init(db_name):
    res = con.cursor()
    res.execute(f"create database if not exists `{db_name}`")
    res.execute(f"use `{db_name}`")
    con.commit()

def check_db_exists(db_name):
    res = con.cursor()
    res.execute("SHOW DATABASES")
    databases = res.fetchall()
    for db in databases:
        if db[0] == db_name:
            return True
    return False

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)