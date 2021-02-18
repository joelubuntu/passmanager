import mysql.connector
from mysql.connector import Error
import datetime
import random
import os
from cryptography.fernet import Fernet

def welcome():
    user_name = os.getlogin()
    time = datetime.datetime.now().hour
    if time <= 12 and time >= 5:
        print('Good morning,')
    elif time <= 17 and time >= 12:
        print('Good afternoon,')
    elif time <= 23 and time >= 17:
        print('Good evening,')
    return user_name

print(welcome())
host = input("Enter database host: ")
user = input("Enter database username: ")
password = input('Enter database password: ')
if host == (''):
    host = ('localhost')
if user == (''):
    user = ('root')
try:
    connection = mysql.connector.connect(host=host,user=user,passwd=password)
    print('Connection established with mysql.')
except:
    print('Invalid credentials.')

def password_generator(host,user,password):
    a = random.choice(['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'])
    b = random.choice(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'])
    c = random.choice([':','!','@','#','$','%','^','&','*','(',')','_','+','|',';','.','`','<','>','?','~'])
    d = random.choice(['1','2','3','4','5','6','7','8','9','0'])
    e = random.choice(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'])
    f = random.choice(['1','2','3','4','5','6','7','8','9','0'])
    g = random.choice([':','!','@','#','$','%','^','&','*','(',')','_','+','|',';','.','`','<','>','?','~'])
    h = random.choice(['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'])
    i = random.choice(['no','hm','lo','py','gg','op','hi'])
    j = random.choice(['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'])
    print("Your random 10 digit password is: \n")
    gen_password = ( a + b + c + d + e + f + g + h + i + j)
    print(gen_password + '\n')
    user_input = input('Would you like to save your password? \n Press y for YES and n for NO: ')
    if user_input.lower() == ('y'):
        user_name = input("Enter your account username: ")
        account = input('This account is of: ')
        add_password = ("INSERT INTO passwords"
                        "(account,username,password)"
                        "VALUES(%s ,%s , %s)")
        connection = mysql.connector.connect(host=host,user=user,passwd=password,database='passmanager')
        data = (account,user_name,gen_password)
        insert(connection,add_password,data)
        print('Saved!')

def menu(host,user,password):
    print('+------------------------------------------------------------------------------------------------+')
    print("|gen pass - it genrates new password of 10 digits.                                               |")
    print("|view pass - it prints saved password if file is not renamed or modified.                        |")
    print("|add - through this feature you can add you custom password in password file.                    |")
    print("|backup - it create a file named backup.txt which contains all your password in encrypted format |")
    print("|decrypt - it decrypt's encrypted backup.txt and save it as decrypted_backupfile.txt             |")
    print('+------------------------------------------------------------------------------------------------+')
    exit = False
    while exit == False:
        user_input = input('Enter your cmd: ')
        if user_input.lower() == ('exit'):
            exit = True
        elif user_input.lower() == ('quit'):
            exit = True
        elif user_input.lower() == ('gen pass'):
            password_generator(host,user,password)
        elif user_input.lower() == ('view pass'):
            view_pass(host,user,password)
        elif user_input.lower() == ('add'):
            add(host,user,password)
        elif user_input.lower() == ('init'):
            init(host,user,password)
        elif user_input.lower() == ('backup'):
            backup(host,user,password)
        elif user_input.lower() == ('decrypt'):
            decryption()

def add(host,user,password):
    user_name = input("Enter your account username: ")
    account = input('This account is of: ')
    gen_password = input('Enter password of: ')
    add_password = ('INSERT INTO passwords VALUES(account,user_name,gen_password)')
    connection = mysql.connector.connect(host=host,user=user,passwd=password,database='passmanager')
    add_data = ("INSERT INTO passwords"
                "(account,username,password)"
                "VALUES(%s,%s,%s)")
    data = (account , user_name , gen_password)
    insert(connection,add_data,data)
    print('passwords added.')

def init(host,user,password):
    connection = mysql.connector.connect(host=host,user=user,passwd=password)
    query = ('CREATE DATABASE passmanager')
    execute(connection , query)
    db_connection = mysql.connector.connect(host=host,user=user,passwd=password,database='passmanager')
    create_passwords_table = ('CREATE TABLE passwords(account VARCHAR(100) NOT NULL , username VARCHAR(100) NOT NULL , password VARCHAR(20) NOT NULL)')
    execute(db_connection,create_passwords_table)
    try:
        Key = Fernet.generate_key()
        f = Fernet(Key)
        with open('key.key' , 'wb') as key:
            key.write(Key)
        print('setup completed!')
    except:
        print('failed init!')

def view_pass(host,user,password):
    connection = mysql.connector.connect(host=host,user=user,passwd=password,database='passmanager')
    query = ('SELECT * FROM passwords')
    cursor = connection.cursor()
    cursor.execute(query)
    for i in cursor:
        print(i)

def execute(connection,query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except:
        print('failed!')

def backup(host,user,password):
    try:
        connection = mysql.connector.connect(host=host,user=user,passwd=password,database='passmanager')
        cursor = connection.cursor()
        query = ('SELECT * FROM passwords')
        cursor.execute(query)
        backup = open('backup.txt','w')
        for (account , username , password) in cursor:
            backup.writelines('{} {} {} {} {} {}'.format(account , '   ' ,username , '   ' , password , '\n\n' ))
        backup.close()
        print('Backup created!')
        encryption()
    except:
        print('Failed!')

def insert(connection,add_data,data):
    cursor = connection.cursor()
    cursor.execute(add_data,data)
    connection.commit()

def encryption():
    try:
        with open('key.key' , 'rb') as key:
            Key = key.read()
        f = Fernet(Key)
        with open('backup.txt' , 'rb') as backup:
            plaintxt = backup.read()
        en = f.encrypt(plaintxt)
        with open('en_backup.txt' , 'wb') as en_backup:
            en_backup.write(en)
        os.remove("backup.txt")
        print('encrypted backup :)')
    except:
        print('failed encryption!')

def decryption():
    try:
        with open('key.key' , 'rb') as key:
            Key = key.read()
        f = Fernet(Key)
        with open('en_backup.txt' , 'rb') as en_backup:
            en_txt = en_backup.read()
        de = f.decrypt(en_txt)
        with open('de_backup.txt' , 'wb') as de_backup:
            de_backup.write(de)
        print("decryption done and saved with file name: de_backup.txt")
    except:
        print('failed decryption!')

try:
    connection = mysql.connector.connect(host=host,user=user,passwd=password,database='passmanager')
    print('Connection established with Database.')
except:
    init(host,user,password)

menu(host,user,password)
