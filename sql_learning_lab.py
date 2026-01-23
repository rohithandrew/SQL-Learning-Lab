import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

con = mysql.connector.connect(
    host = os.getenv('DB_HOST'),
    user = os.getenv('DB_USER'),
    password = os.getenv('DB_PASS'),
    database = os.getenv('DB_NAME')
)

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

def user_actions(actions):
    res = con.cursor()
    res.execute(actions)
    result = res.fetchall()
    print(result)
    con.commit()

def check_db_exists(db_name):
    res = con.cursor()
    res.execute("SHOW DATABASES")
    databases = res.fetchall()
    for db in databases:
        if db[0] == db_name:
            return True
    return False


while True:

    exit_main_loop = False

    print("Choose Action!")
    print("1. New User? Register")
    print("2. Already have an account? Login")

    choice = int(input("Enter your choice (1 or 2): "))

    if choice == 1:
        print("Register Now!")

        while True:
        
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            if check_login(username.lower(), password):
                print("You are already registered! Please login.")
                break
            elif check_username(username.lower()):
                print("Username already exists!")
            else:
                register(username.lower(), password)
                break

    elif choice == 2:

        print("Login Now!")

        while True:

            username = input("Enter your username: ")
            password = input("Enter your password: ")

            if not check_username(username.lower()):
                print("Username does not exist! Please register first.")
                break
            else:

                if check_login(username.lower(), password):
                    print("Login Successful!")
                    exit_main_loop = True
                    break
                else:
                    print("Incorrect password! Please try again.")

    if exit_main_loop:
        break

if not check_db_exists(username.lower() + "_db"):
    db_name = username.lower() + "_db"
    print(f"Initializing database: {db_name}")
    db_init(db_name)
    print(f"Database '{db_name}' initialized.")

    while True:
        blocked_words = ['SHOW DATABASES', 'SHOW SCHEMAS', 'USE ', 'DROP DATABASE', 'CREATE DATABASE']
        action = input("Enter your SQL action (or type 'exit' to quit): ")
        if any (word in action.upper() for word in blocked_words):
            print("This action is not allowed.")
            continue
        if action.lower() == 'exit':
            print("Exiting the program.")
            break
        result = user_actions(action)
        
else:
    db_name = username.lower() + "_db"
    print(f"Using existing database: {db_name}")
    db_init(db_name)

    while True:
        blocked_words = ['SHOW DATABASES', 'SHOW SCHEMAS', 'USE ', 'DROP DATABASE', 'CREATE DATABASE']
        action = input("Enter your SQL action (or type 'exit' to quit): ")
        if any (word in action.upper() for word in blocked_words):
            print("This action is not allowed.")
            continue
        if action.lower() == 'exit':
            print("Exiting the program.")
            break
        result = user_actions(action)