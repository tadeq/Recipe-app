import os
from flask import Flask, request, render_template, redirect, url_for
import requests
from datetime import datetime
from model import User, Product, Dish, HistoryEntry, ALL_LABELS, DIET_LABELS, HEALTH_LABELS
from db_connectivity import Dao

from authlib.client import OAuth2Session
import google.oauth2.credentials
import googleapiclient.discovery
import google_auth

SECRET_KEY = os.urandom(24)

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.register_blueprint(google_auth.app)

results = []
user = None

with open('auth_api.txt') as auth_file:
    app_id = auth_file.readline().strip()
    app_key = auth_file.readline().strip()


def build_request(query, health_labels, diet_labels):
    api_request = 'https://api.edamam.com/search?to=100&app_id={}&app_key={}'.format(app_id, app_key)
    api_request += "&q={}".format(query)
    for label in health_labels:
        api_request += "&health={}".format(label)
    for label in diet_labels:
        api_request += "&diet={}".format(label)
    return api_request


@app.route('/', methods=['GET'])
def index():
    global user
    if google_auth.is_logged_in() and user is None:
        user_info = google_auth.get_user_info()
        user = dao.get_user_by_id(user_info['id'])
        if user is None:
            user = dao.create_user(
                User(user_info['id'], user_info['given_name'], user_info['family_name'], user_info['picture']))
    elif not google_auth.is_logged_in() and user is not None:
        user = None
    return render_template('search_layout.html', labels=ALL_LABELS, profile=user)


@app.route('/profile', methods=['GET'])
def profile():
    return render_template('profile.html', profile=user)


@app.route('/profile/history', methods=['GET'])
def profile_history():
    return render_template('history.html', profile=user)


@app.route('/profile/favourites', methods=['GET'])
def profile_favourites():
    return render_template('favourites.html', profile=user)


@app.route('/profile/products', methods=['GET', 'POST'])
def profile_products():
    if request.method == 'POST':
        dao.add_product(user,
                        Product(request.form.get('name'), request.form.get('quantity'), request.form.get('unit')))
    return render_template('products.html', profile=user)


@app.route('/profile/products/delete', methods=['POST'])
def delete_product():
    dao.delete_product(user, dao.get_product_by_name(request.form.get('product_name')))
    return redirect(url_for('profile_products'))


@app.route('/recipes', methods=['GET'])
def recipe_results():
    global results
    query = request.args['query']
    labels = [label for label in ALL_LABELS if request.args.get(label) is not None]
    health_labels = list(filter(lambda l: l in HEALTH_LABELS, labels))
    diet_labels = list(filter(lambda l: l in DIET_LABELS, labels))
    api_request = build_request(query, health_labels, diet_labels)
    if user is not None:
        if query in [entry.query for entry in user.history]:
            dao.delete_entry(user, query)
        dao.add_history_entry(user, HistoryEntry(query, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    response = requests.get(api_request)
    results = [Dish(hit['recipe']) for hit in response.json()['hits']] if response.status_code == 200 else []
    return render_template('recipes.html', labels=ALL_LABELS, recipes=results, profile=user)


@app.route('/recipes/<recipe_id>', methods=['GET', 'POST'])
def recipe_details(recipe_id):
    recipe = None
    for res in results:
        if res.id == recipe_id:
            recipe = res
    if request.method == 'POST':
        if user is not None:
            if recipe is not None and recipe not in user.favourites:
                dao.add_favourite_dish(user, recipe)
    elif request.method == 'GET' and recipe is None:
        recipe = dao.get_dish_by_id(recipe_id)
    return render_template('recipe.html', labels=ALL_LABELS, recipe=recipe, profile=user)


if __name__ == '__main__':
    dao = Dao()
    # user = dao.create_user(User(1, 'John', 'Doe'))
    # user = dao.get_user_by_id(1)
    # user.products = dao.get_products_by_user(user)
    # user.history = dao.get_history_entries_by_user(user)
    # user.favourites = dao.get_dishes_by_user(user)
    app.run()
