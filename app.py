from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime
from model import User, Product, Dish, HistoryEntry, diet_labels

app = Flask(__name__)

with open('response.json') as res_file:
    response = json.load(res_file)

results = [Dish(hit['recipe']) for hit in response['hits']]

mock_user = User(1, 'Test', 'User')
mock_products = [Product('Chicken', 2, 'kg'), Product('Butter', 200, 'g')]
mock_user.products = mock_products


@app.route('/')
def search():
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


@app.route('/profiles/<profile_id>/products', methods=['GET', 'POST'])
def profile_products(profile_id):
    if request.method == 'POST':
        mock_user.products.append(
            Product(request.form.get('name'), request.form.get('quantity'), request.form.get('unit')))
    return render_template('products.html', profile=mock_user)


@app.route('/recipes', methods=['GET', 'POST'])
def recipe_results():
    query = request.form['query']
    if query in mock_user.history:
        mock_user.history.remove(query)
    mock_user.history.append(HistoryEntry(query, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    return render_template('recipes.html', labels=diet_labels, recipes=results)


@app.route('/recipes/<recipe_id>', methods=['GET', 'POST'])
def recipe_details(recipe_id):
    # TODO if the recipe was chosen from the favourites -> get it from db, if from search results -> get it from results
    for res in results:
        if res.id == recipe_id:
            recipe = res
    if request.method == 'POST':
        if recipe not in mock_user.favourites:
            mock_user.favourites.append(recipe)
    return render_template('recipe.html', labels=diet_labels, recipe=recipe)


if __name__ == '__main__':
    app.run()
