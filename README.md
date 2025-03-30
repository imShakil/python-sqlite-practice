# Python SQLite Cheat-Sheet
[![GitHub stars](https://img.shields.io/github/stars/imshakil/python-sqlite-practice)](https://github.com/imshakil/python-sqlite-practice/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/imshakil/python-sqlite-practice)](https://github.com/imshakil/python-sqlite-practice/network)
[![GitHub issues](https://img.shields.io/github/issues/imshakil/python-sqlite-practice)](https://github.com/imshakil/python-sqlite-practice/issues)
[![GitHub License](https://img.shields.io/github/license/imShakil/python-sqlite-practice)](https://github.com/imshakil/python-sqlite-practice)
[![Twitter](https://img.shields.io/twitter/url?style=social&url=https%3A%2F%2Fgithub.com%2Fimshakil%2Fpython-sqlite-practice)](https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2Fimshakil%2Fpython-sqlite-practice)

<!-- [![HitCount](https://hits.dwyl.com/imshakil/python-sqlite-practice.svg?style=flat-square)](http://hits.dwyl.com/imshakil/python-sqlite-practice)
#[![HitCount](https://hits.dwyl.com/imshakil/python-sqlite-practice.svg?style=flat-square&show=unique)](http://hits.dwyl.com/imshakil/python-sqlite-practice)
-->

SQLite3 is a very easy to use database engine. It is self-contained, serverless, zero-configuration and transactional.
It is very fast and lightweight, and the entire database is stored in a single disk file. It is used in a lot of
applications as internal data storage. The Python Standard Library includes a module called "sqlite3" intended for
working with this database. This module is a SQL interface compliant with the DB-API 2.0 specification.

**Table of Contents**
- [SQLite Python Module](#import-sqlite-module)
- [Connect and Creating Database](#connect-and-create-database)
- [CREATE and DROP TABLE](#creating-create-and-deleting-drop-tables)
- [INSERT INTO TABLE](#inserting-insert-data-into-the-database)
- [SELECT FROM (data retrieving)](#retrieving-data-select-from-database)
- [UPDATE and DELETE FROM](#updating-update-and-deleting-delete-data)
- [SQLite Transaction](#using-sqlite-transactions)
- [Handling SQLite Exceptions](#sqlite-database-exceptions)
- [SQLite Row Factory](#sqlite-row-factory-and-data-types)

## Import SQLite Module

```python
import random
import sqlite3
```


## Connect and Create Database 
We use the function ```sqlite3.connect``` to connect to the database. We can use the argument ```:memory:``` to create 
a temporary DB in the RAM or pass the name of a file to open or create it.


```python
# create database in memory
# db = sqlite3.connect(':memory:')

# create database into directory
db = sqlite3.connect("./data/test.db")

# get a cursor object
cursor = db.cursor()
```


## Creating (```CREATE```) and Deleting (```DROP```) Tables
In order to make any operation with the database we need to get a cursor object and pass the SQL statements to the 
cursor object to execute them. Finally it is necessary to commit the changes. We are going to create a users table with 
name, phone, email and password columns.


```python
# DROP TABLE
cursor.execute("""DROP TABLE IF EXISTS users""")

# CREATE TABLE
cursor.execute(
    """CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    phone TEXT,
                    email TEXT unique,
                    password TEXT
            )"""
)

db.commit()
```

## Inserting (```INSERT```) Data into the Database
To insert data we use the cursor to execute the query. If you need values from Python variables it is recommended 
to use the "?" placeholder. Never use string operations or concatenation to make your queries because is very insecure.
In this example we are going to insert two users in the database, their information is stored in python variables.

```python
name = 'Halim'
phone = "01234567890"
email = "halim@email.com"
password = "ha1234"
cursor.execute(
    """INSERT INTO users(name, phone, email, password) VALUES (?,?,?,?)""",
    (name, phone, email, password),
)
db.commit()
```


The values of the Python variables are passed inside a tuple. 
Another way to do this is passing a dictionary using the ```:key name``` placeholder:

```python
name = "Alim"
phone = "01234567890"
email = "alim@email.com"
password = "al1234"
cursor.execute(
    """INSERT INTO users(name, phone, email, password) VALUES (:name, :phone, :email, :password)""",
    {
        "name": name,
        "phone": phone,
        "email": email,
        "password": password,
    },
)
db.commit()

# use list of users for inserting multiple user info
users = [
    (
        "Name " + str(i),
        str(random.randint(10000000, 1000000000)),
        "name" + str(i) + "@email.com",
        str(random.randint(10000, 90000)),
    )
    for i in range(10)
]

cursor.executemany(
    """INSERT INTO users(name, phone, email, password) VALUES (?, ?, ?, ?)""", users
)
db.commit()
```

### Get Last Row ID

If you need to get the id of the row you just inserted use ```lastrowid```

```python
print(f"last row id: {cursor.lastrowid}")
```

## Retrieving Data (```SELECT```) from Database
To retrieve data, execute the query against the cursor object and then use ```fetchone()``` to retrieve a single row or 
```fetchall()``` to retrieve all the rows and ```fetchmany()``` to retrieve a particular number or rows.
(note: retrieve rows fetched as a list where each row as a tuple)

```python
cursor.execute("""SELECT name, phone, email FROM users""")
user1 = cursor.fetchone()
print(user1)

user_many = cursor.fetchmany(5)
print(user_many)

user_all = cursor.fetchall()
print(user_all)
```

The cursor object works as an iterator, invoking ```fetchall()``` automatically

```python
cursor.execute("""SELECT name, email, phone FROM users""")
for row in cursor:
    print(f"name: {row[0]} email: {row[1]} phone: {row[2]}")
```

To retrieve data with conditions, use again the "?" placeholder

```python
user_id = 5
cursor.execute("""SELECT name, email, phone FROM users WHERE id=?""", (user_id,))
print(cursor.fetchone())
```

## Updating (```UPDATE```) and Deleting (```DELETE```) Data
The procedure to update or delete data is the same as inserting data

```python
# update user phone with id = 5
cursor.execute("""UPDATE users SET phone = ? WHERE id = ?""", ("01710567890", user_id))
db.commit()

# delete user row with id = 8
cursor.execute("""DELETE FROM users WHERE id = ?""", (8,))
db.commit()
```

## Using SQLite Transactions
Transactions are an useful property of the database systems. It ensures the atomicity of the Database. Use ```commit()``` 
method to save the changes and ```rollback()``` method to roll back any change to the database since the last call to commit.

```python
# update user phone with id = 5
cursor.execute("""UPDATE users SET phone = ? WHERE id = ?""", ("01712567890", user_id))
db.rollback()
```

Please remember to always call commit to save the changes. If you close the connection using close or the connection to 
the file is lost (maybe the program finishes unexpectedly), not committed changes will be lost.


## SQLite Database Exceptions
For best practices always surround the database operations with a try clause or a context manager.

```python
try:
    # create or connect database
    db = sqlite3.connect("./data/test.db")

    # get a cursor object
    cursor = db.cursor()

    # check if a table 'users' does exist or not and create it
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT, phone TEXT, email TEXT unique, password TEXT)"""
    )
    # commit to save the changes
    db.commit()

except Exception as e:
    # rollback any change if something goes wrong
    db.rollback()
    raise e
finally:
    db.close()
```

### Check Integrity Error
We can use the Connection object as context manager to automatically commit or rollback transactions

```python
name1 = "Mobarak"
phone1 = "3366858"
email1 = "imshakil@github.com"
# A very secure password
password1 = "12345"
try:
    db = sqlite3.connect("./data/test.db")
    with db:
        db.execute(
            """INSERT INTO users (name, phone, email, password) VALUES (?, ?, ?, ?)""",
            (name1, phone1, email1, password1),
        )
except sqlite3.IntegrityError:
    print("Data already exists")
finally:
    db.close()
```

In the example above if the insert statement raises an exception, the transaction will be rolled back and the message 
gets printed; otherwise the transaction will be committed. Please note that we call execute on the db object, not the 
cursor object.


## SQLite Row Factory and Data Types 
The following table shows the relation between SQLite datatypes and Python datatypes:

- None type is converted to NULL
- int type is converted to INTEGER
- float type is converted to REAL
- str type is converted to TEXT
- bytes type is converted to BLOB

The row factory class ```sqlite3.Row``` is used to access the columns of a query by name instead of by index.

```python
db = sqlite3.connect("./data/test.db")
db.row_factory = sqlite3.Row
cursor = db.cursor()
cursor.execute("""SELECT name, email, phone FROM users""")
for row in cursor:
    print(f"name : {row[0]}, email: {row[1]}, phone: {row[2]}")

# close database connection
db.close()
```

> Thanks to Andres Torres for awesome blog post <br> 
> Source: https://www.pythoncentral.io/introduction-to-sqlite-in-python/
