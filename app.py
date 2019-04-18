from flask import Flask, render_template, request, redirect, url_for
from itertools import count
import json
from model import User, Product, Dish, diet_labels

app = Flask(__name__)

with open('response.json') as res_file:
    response = json.load(res_file)

counter = count()
results = [Dish(next(counter), hit['recipe']) for hit in response['hits']]

mock_user = User(1, 'Test', 'User')
mock_products = [Product('Chicken', 2, 'kg').__dict__, Product('Butter', 200, 'g').__dict__]
mock_user.products = mock_products
mock_user = mock_user.__dict__


@app.route('/')
def index():
    return render_template('search_layout.html', labels=diet_labels)


@app.route('/profiles/<profile_id>')
def profile(profile_id):
    return render_template('profile.html', profile=mock_user)


@app.route('/profiles/<profile_id>/history')
def profile_history(profile_id):
    return render_template('history.html', profile=mock_user)


@app.route('/profiles/<profile_id>/favourites')
def profile_favourites(profile_id):
    return render_template('favourites.html', profile=mock_user)


@app.route('/profiles/<profile_id>/products')
def profile_products(profile_id):
    return render_template('products.html', profile=mock_user)


@app.route('/recipes', methods=['GET', 'POST'])
def recipe_results():
    print([request.form.get(label) for label in diet_labels])
    return render_template('recipes.html', recipes=results)


@app.route('/recipes/<recipe_id>')
def recipe_details(recipe_id):
    return render_template('recipe.html', recipe=results[int(recipe_id)])


if __name__ == '__main__':
    app.run()
