import sqlite3
import json
from model import Dish, HistoryEntry, Product, User


class DbConnection:
    def __init__(self):
        self.connection = sqlite3.connect(':memory:')  # only for test purposes
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Users (
                            id integer PRIMARY KEY,
                            firstname text,
                            surname text
                            )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Products (
                            product_name text,
                            quantity real,
                            unit text,
                            user_id integer,
                            FOREIGN KEY (user_id) REFERENCES Users (id)
                            )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS History_entries(
                            query text,
                            date_time text,
                            user_id integer,
                            FOREIGN KEY (user_id) REFERENCES Users (id)
                            )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Dishes(
                            id text PRIMARY KEY,
                            json_dish text,
                            user_id integer,
                            FOREIGN KEY (user_id) REFERENCES Users (id)
                            )""")

    # TODO add google account identifier
    def create_user(self, user):
        with self.connection:
            self.cursor.execute('INSERT INTO Users VALUES (:firstname, :surname)',
                                {'firstname': user.name, 'surname': user.surname})

    def create_product(self, user_id, product):
        with self.connection:
            self.cursor.execute('INSERT INTO Products VALUES (:product_name, :quantity, :unit, :user_id)',
                                {'product_name': product.name, 'quantity': product.quantity, 'unit': product.unit,
                                 'user_id': user_id})

    def create_history_entry(self, user_id, entry):
        with self.connection:
            self.cursor.execute('INSERT INTO History_entries VALUES (:query, :date_time, :user_id)',
                                {'query': entry.query, 'date_time': entry.date_time, 'user_id': user_id})

    def create_dish(self, user_id, dish):
        with self.connection:
            self.cursor.execute(
                """INSERT INTO Dishes VALUES (:id, :json_dish, :user_id)""",
                {'id': dish.id, 'json_dish': json.dumps(dish.__dict__), 'user_id': user_id})

    # TODO change to get by google identifier
    def get_user_by_id(self, user_id):
        self.cursor.execute('SELECT * FROM Users WHERE id = :user_id', {'user_id': user_id})
        user = self.cursor.fetchone()
        return User(user[0], user[1], user[2])

    def get_products_by_user(self, user_id):
        self.cursor.execute('SELECT * FROM Products WHERE user_id = :user_id', {'user_id': user_id})
        products = self.cursor.fetchall()
        return [Product(p[0], p[1], p[2]) for p in products]

    def get_history_entries_by_user(self, user_id):
        self.cursor.execute('SELECT * FROM History_entries WHERE user_id = :user_id', {'user_id': user_id})
        entries = self.cursor.fetchall()
        return [HistoryEntry(e.query, e.date_time) for e in entries[0]]

    def get_dishes_by_user(self, user_id):
        self.cursor.execute('SELECT json_dish FROM Dishes WHERE user_id = :user_id', {'user_id': user_id})
        json_dishes = self.cursor.fetchall()
        return [Dish(json.loads(json_dish)) for json_dish in json_dishes[0]]

    def edit_product(self, user_id, product):
        with self.connection:
            self.cursor.execute("""UPDATE Products SET product_name = :product_name, quantity = :quantity, unit = :unit 
            WHERE user_id = :user_id""", {'product_name': product.name, 'quantity': product.quantity,
                                          'unit': product.unit, 'user_id': user_id})

    def delete_product(self, user_id, product):
        with self.connection:
            self.cursor.execute("""DELETE FROM Products WHERE user_id = :user_id AND product_name = :product_name 
            AND quantity = :quantity AND unit = :unit""", {'user_id': user_id, 'product_name': product.name,
                                                           'quantity': product.quantity, 'unit': product.unit})

    def delete_dish(self, user_id, dish):
        with self.connection:
            self.cursor.execute("""DELETE FROM Dishes WHERE user_id = :user_id AND id = :id""",
                                {'user_id': user_id, 'id': dish.id})
