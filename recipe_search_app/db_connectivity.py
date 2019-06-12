import sqlite3
import json
from model import Dish, HistoryEntry, Product, User


class Dao:
    def __init__(self):
        self.connection = sqlite3.connect('recipe_app.db', check_same_thread=False)  # only for test purposes
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Users (
                            id text PRIMARY KEY,
                            firstname text,
                            surname text,
                            img_url text
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
            self.cursor.execute('INSERT INTO Users VALUES (:id, :firstname, :surname, :img_url)',
                                {'id': user.id, 'firstname': user.name, 'surname': user.surname,
                                 'img_url': user.image_url})
        return self.get_user_by_id(user.id)

    def add_product(self, user, product):
        with self.connection:
            self.cursor.execute('INSERT INTO Products VALUES (:product_name, :quantity, :unit, :user_id)',
                                {'product_name': product.name, 'quantity': product.quantity, 'unit': product.unit,
                                 'user_id': user.id})
            user.products.append(product)

    def add_history_entry(self, user, entry):
        with self.connection:
            self.cursor.execute('INSERT INTO History_entries VALUES (:query, :date_time, :user_id)',
                                {'query': entry.query, 'date_time': entry.date_time, 'user_id': user.id})
            user.history.append(entry)

    def add_favourite_dish(self, user, dish):
        with self.connection:
            self.cursor.execute(
                'INSERT INTO Dishes VALUES (:id, :json_dish, :user_id)',
                {'id': dish.id, 'json_dish': json.dumps(dish.__dict__), 'user_id': user.id})
            user.favourites.append(dish)

    def get_user_by_id(self, user_id):
        self.cursor.execute('SELECT * FROM Users WHERE id = :user_id', {'user_id': user_id})
        user = self.cursor.fetchone()
        if user is not None:
            found_user = User(user[0], user[1], user[2], user[3])
            found_user.products = self.get_products_by_user(found_user)
            found_user.favourites = self.get_dishes_by_user(found_user)
            found_user.history = self.get_history_entries_by_user(found_user)
            return found_user
        return None

    def get_dish_by_id(self, dish_id):
        self.cursor.execute('SELECT json_dish FROM Dishes WHERE id = :dish_id', {'dish_id': dish_id})
        json_dish = self.cursor.fetchone()
        if json_dish is not None:
            return Dish(json.loads(json_dish[0]))
        return None

    def get_products_by_user(self, user):
        self.cursor.execute('SELECT * FROM Products WHERE user_id = :user_id', {'user_id': user.id})
        products = self.cursor.fetchall()
        return [Product(p[0], p[1], p[2]) for p in products]

    def get_product_by_name(self, product_name):
        self.cursor.execute('SELECT * FROM Products WHERE product_name=:product_name', {'product_name': product_name})
        product = self.cursor.fetchone()
        if product is not None:
            return Product(product[0], product[1], product[2])
        return None

    def get_history_entries_by_user(self, user):
        self.cursor.execute('SELECT * FROM History_entries WHERE user_id = :user_id', {'user_id': user.id})
        entries = self.cursor.fetchall()
        entries = [HistoryEntry(entry[0], entry[1]) for entry in entries]
        return [HistoryEntry(e.query, e.date_time) for e in entries]

    def get_dishes_by_user(self, user):
        self.cursor.execute('SELECT json_dish FROM Dishes WHERE user_id = :user_id', {'user_id': user.id})
        json_dishes = self.cursor.fetchall()
        return [Dish(json.loads(json_dish[0])) for json_dish in json_dishes]

    # CURRENTLY UNUSED
    # def edit_product(self, user, product):
    #     with self.connection:
    #        self.cursor.execute("""UPDATE Products SET product_name = :product_name, quantity = :quantity, unit = :unit
    #         WHERE user_id = :user_id""", {'product_name': product.name, 'quantity': product.quantity,
    #                                       'unit': product.unit, 'user_id': user.id})

    def delete_product(self, user, product):
        with self.connection:
            self.cursor.execute("""DELETE FROM Products WHERE user_id = :user_id AND product_name = :product_name 
        AND quantity = :quantity AND unit = :unit""", {'user_id': user.id, 'product_name': product.name,
                                                       'quantity': product.quantity, 'unit': product.unit})
            to_remove = []
            for p in user.products:
                if p.name == product.name and p.quantity == product.quantity and p.unit == product.unit:
                    to_remove.append(p)
            for prod_to_remove in to_remove:
                user.products.remove(prod_to_remove)

    def delete_favourite_dish(self, user, dish):
        with self.connection:
            self.cursor.execute('DELETE FROM Dishes WHERE user_id = :user_id AND id = :id',
                                {'user_id': user.id, 'id': dish.id})
            user.favourites.remove(dish)

    def delete_entry(self, user, query):
        with self.connection:
            self.cursor.execute('DELETE FROM History_entries WHERE user_id = :user_id AND query = :query',
                                {'user_id': user.id, 'query': query})
            user.remove_history_entry_by_query(query)
