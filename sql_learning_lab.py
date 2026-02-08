import os
from dotenv import load_dotenv
import mysql.connector
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

load_dotenv()

def get_connection(db_name: str = None):
    params = {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASS'),
    }
    if db_name:
        params['database'] = db_name
    else:
        default_db = os.getenv('DB_NAME')
        if default_db:
            params['database'] = default_db
    return mysql.connector.connect(**params)

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
def execute_sql(username: str, query: SQLQuery, credentials: UserCredentials):
    if not check_login(credentials.username.lower(), credentials.password):
        raise HTTPException(status_code=401, detail="Invalid credentials!")
    
    if credentials.username.lower() != username.lower():
        raise HTTPException(status_code=401, detail="Username mismatch!")
    
    blocked_words = ['SHOW DATABASES', 'SHOW SCHEMAS', 'USE ', 'DROP DATABASE', 'CREATE DATABASE']
    if any(word in query.query.upper() for word in blocked_words):
        raise HTTPException(status_code=403, detail="This action is not allowed.")
    
    db_name = username.lower() + "_db"
    db_init(db_name)

    conn = get_connection(db_name)
    cur = conn.cursor()
    try:
        cur.execute(query.query)
        try:
            result = cur.fetchall()
        except Exception:
            result = None
        conn.commit()
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error executing query: {str(e)}")
    finally:
        cur.close()
        conn.close()

def register(username, password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = "insert into login_credentials (username, password) values (%s, %s)"
        user = (username , password)
        cur.execute(sql, user)
        conn.commit()
        print("Registration Successful!")
    finally:
        cur.close()
        conn.close()

def check_login(username, password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = "select * from login_credentials where username = %s and password = %s"
        user = (username , password)
        cur.execute(sql, user)
        result = cur.fetchone()
        return bool(result)
    finally:
        cur.close()
        conn.close()

def check_username(username):
    conn = get_connection()
    cur = conn.cursor()
    try:
        sql = "select * from login_credentials where username = %s"
        user = (username ,)
        cur.execute(sql, user)
        result = cur.fetchone()
        return bool(result)
    finally:
        cur.close()
        conn.close()
    
def db_init(db_name):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(f"create database if not exists `{db_name}`")
        conn.commit()
    finally:
        cur.close()
        conn.close()

def check_db_exists(db_name):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SHOW DATABASES")
        databases = cur.fetchall()
        for db in databases:
            if db[0] == db_name:
                return True
        return False
    finally:
        cur.close()
        conn.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)