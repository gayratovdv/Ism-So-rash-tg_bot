import sqlite3

db = sqlite3.connect("database.db", check_same_thread=False)  # DB ga ulash uchun, agar bo'lmasa yaratilishi uchun
cursor = db.cursor()


async def db_start():
    """
    Database yaratilishi uchun kod execute metodi orqali bajariladi
    """
    print('Database initialising...')
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS products(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    price INTEGER)
                    """
                   )
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    surname TEXT)
                    """
                   )

    db.commit()  # SQL kodimiz ushlashi uchun, tepadagi kodlarni db ga yuborishimiz kera, uni commit() metodi orqali amalga oshiramiz
    print("Database Initialized")


# create user
async def create_user(name, surname):
    cursor.execute("INSERT INTO users (name, surname) VALUES (?, ?)", (name, surname))
    db.commit()

async def create_product(name, price):
    cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
    db.commit()


# SELECT
async def select_products():
    cursor.execute("SELECT * FROM products")
    return cursor.fetchall()  # bor malumotlani olishimiz uchun fetchall() metodini ishlatamiz


async def select_users():
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()
