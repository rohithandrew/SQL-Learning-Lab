# User Authentication & Database Management with Python and MySQL

A command-line application that lets users register and log in using MySQL as the backend, securely loading credentials from a `.env` file via `python-dotenv`. It supports creating a database and table dynamically and running SQL queries interactively.



## Features

- **User Registration & Login**: Register new users and authenticate existing ones.
- **Database Initialization**: Create databases and tables if they don't exist.
- **Interactive SQL Execution**: Run arbitrary SQL commands after login.
- **Environment Variables**: Securely manage DB credentials using `.env`.
- **Uses `mysql-connector-python`** for MySQL connection.
- Simple, menu-driven CLI interface.



## Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install dependencies**

   ```bash
   pip install mysql-connector-python python-dotenv
   ```

3. **Create a `.env` file**

   Add your MySQL credentials:

   ```
   DB_HOST=localhost
   DB_USER=your_mysql_username
   DB_PASS=your_mysql_password
   DB_NAME=your_default_database
   ```



## Usage

Run the Python script:

```bash
python your_script_name.py
```

- Choose **1** to register as a new user.
- Choose **2** to login as an existing user.
- After login, create/connect to a database and table.
- Execute SQL queries interactively.
- Type `'exit'` to quit.



## Security Notes

- Passwords are stored in plain text; for production, add password hashing.
- Keep your `.env` file out of version control (add to `.gitignore`).
- Use a MySQL user with restricted privileges, not root.



## Future Improvements

- Add password hashing and stronger authentication.
- Input validation and protection against SQL injection.
- Role-based access control.
- Develop a GUI or web interface.



## License

MIT License
