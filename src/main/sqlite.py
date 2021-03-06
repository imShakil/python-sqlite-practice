################################
# Using Python's SQLite Module #
################################

"""
SQLite3 is a very easy to use database engine. It is self-contained, serverless, zero-configuration and transactional.
It is very fast and lightweight, and the entire database is stored in a single disk file. It is used in a lot of
applications as internal data storage. The Python Standard Library includes a module called "sqlite3" intended for
working with this database. This module is a SQL interface compliant with the DB-API 2.0 specification.
"""

import random
import sqlite3
from src.main.user import USER


###########################
# connect/create database #
###########################

"""
We use the function sqlite3.connect to connect to the database. We can use the argument ":memory:" to create a 
temporary DB in the RAM or pass the name of a file to open or create it.
"""

# create database in memory
# db = sqlite3.connect(':memory:')

# create database into directory
db = sqlite3.connect("./data/test.db")

# get a cursor object
cur = db.cursor()


################################################
# Creating (CREATE) and Deleting (DROP) Tables #
################################################

"""
In order to make any operation with the database we need to get a cursor object and pass the SQL statements to the 
cursor object to execute them. Finally it is necessary to commit the changes. We are going to create a users table with 
name, phone, email and password columns.
"""

"""
DROP TABLE
"""

cur.execute("""DROP TABLE IF EXISTS users""")

"""
CREATE
"""

cur.execute(
    """CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    phone TEXT,
                    email TEXT unique,
                    password TEXT
            )"""
)

db.commit()


#############################################
# Inserting (INSERT) Data into the Database #
#############################################


"""
To insert data we use the cursor to execute the query. If you need values from Python variables it is recommended 
to use the "?" placeholder. Never use string operations or concatenation to make your queries because is very insecure.
In this example we are going to insert two users in the database, their information is stored in python variables.
"""

user = USER("Halim", "01234567890", "halim@email.com", "ha1234")
cur.execute(
    """INSERT INTO users(name, phone, email, password) VALUES (?,?,?,?)""",
    (user.name, user.phone, user.email, user.password),
)
db.commit()

"""
The values of the Python variables are passed inside a tuple. 
Another way to do this is passing a dictionary using the ":key name" placeholder:
"""
user = USER("Alim", "01234567890", "alim@email.com", "al1234")
cur.execute(
    """INSERT INTO users(name, phone, email, password) VALUES (:name, :phone, :email, :password)""",
    {
        "name": user.name,
        "phone": user.phone,
        "email": user.email,
        "password": user.password,
    },
)
db.commit()

"""
use list of users for inserting multiple user info
"""
users = [
    (
        "Name " + str(i),
        str(random.randint(10000000, 1000000000)),
        "name" + str(i) + "@email.com",
        str(random.randint(10000, 90000)),
    )
    for i in range(10)
]

cur.executemany(
    """INSERT INTO users(name, phone, email, password) VALUES (?, ?, ?, ?)""", users
)
db.commit()


###################################
# to get the last inserted row id #
###################################

"""
If you need to get the id of the row you just inserted use lastrowid
"""
print(f"last row id: {cur.lastrowid}")


########################################
# Retrieving Data (SELECT) with SQLite #
########################################

"""
To retrieve data, execute the query against the cursor object and then use fetchone() to retrieve a single row or 
fetchall() to retrieve all the rows.
(note: retrieve rows fetched as a list where each row as a tuple)
"""

cur.execute("""SELECT name, phone, email FROM users""")
user1 = cur.fetchone()
print(user1)

user_many = cur.fetchmany(5)
print(user_many)

user_all = cur.fetchall()
print(user_all)

"""
The cursor object works as an iterator, invoking fetchall() automatically
"""
cur.execute("""SELECT name, email, phone FROM users""")
for row in cur:
    print(f"name: {row[0]} email: {row[1]} phone: {row[2]}")

"""
To retrieve data with conditions, use again the "?" placeholder
"""
user_id = 5
cur.execute("""SELECT name, email, phone FROM users WHERE id=?""", (user_id,))
print(cur.fetchone())


################################################
# Updating (UPDATE) and Deleting (DELETE) Data #
################################################

"""
The procedure to update or delete data is the same as inserting data
"""
# update user phone with id = 5
cur.execute("""UPDATE users SET phone = ? WHERE id = ?""", ("01710567890", user_id))
db.commit()

# delete user row with id = 8
cur.execute("""DELETE FROM users WHERE id = ?""", (8,))
db.commit()


#############################
# Using SQLite Transactions #
#############################

"""
Transactions are an useful property of the database systems. It ensures the atomicity of the Database. Use commit() 
method to save the changes and rollback() method to roll back any change to the database since the last call to commit.
"""
# update user phone with id = 5
cur.execute("""UPDATE users SET phone = ? WHERE id = ?""", ("01712567890", user_id))
db.rollback()

"""
Please remember to always call commit to save the changes. If you close the connection using close or the connection to 
the file is lost (maybe the program finishes unexpectedly), not committed changes will be lost.
"""

##############################
# SQLite Database Exceptions #
##############################

"""
For best practices always surround the database operations with a try clause or a context manager.
"""

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

# check integrity error
"""
We can use the Connection object as context manager to automatically commit or rollback transactions
"""

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

"""
In the example above if the insert statement raises an exception, the transaction will be rolled back and the message 
gets printed; otherwise the transaction will be committed. Please note that we call execute on the db object, not the 
cursor object.
"""

#####################################
# SQLite Row Factory and Data Types #
#####################################

"""
The following table shows the relation between SQLite datatypes and Python datatypes:

- None type is converted to NULL
- int type is converted to INTEGER
- float type is converted to REAL
- str type is converted to TEXT
- bytes type is converted to BLOB

The row factory class sqlite3.Row is used to access the columns of a query by name instead of by index.
"""

db = sqlite3.connect("./data/test.db")
db.row_factory = sqlite3.Row
cursor = db.cursor()
cursor.execute("""SELECT name, email, phone FROM users""")
for row in cursor:
    print(f"name : {row[0]}, email: {row[1]}, phone: {row[2]}")

# close database connection
db.close()


###########################################
# Using SQLite's date and datetime Types #
###########################################

"""
Sometimes we need to insert and retrieve some date and datetime types in our SQLite3 database. When you execute the 
insert query with a date or datetime object, the sqlite3 module calls the default adapter and converts them to an ISO 
form at. When you execute a query in order to retrieve those values, the sqlite3 module is going to return a string object
"""
