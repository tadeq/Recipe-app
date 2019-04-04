from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    pass


@app.route('/profiles/<profile_id>')
def profile(profile_id):
    pass


@app.route('/profiles/<profile_id>/history')
def profile_history(profile_id):
    pass


@app.route('/profiles/<profile_id>/favourites')
def profile_favourites(profile_id):
    pass


@app.route('/profiles/<profile_id>/products')
def profile_products(profile_id):
    pass


@app.route('/<recipe_id>')
def recipe_details(recipe_id):
    pass


if __name__ == '__main__':
    app.run()
