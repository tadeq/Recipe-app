import os
from flask import Flask, render_template, session, jsonify, redirect, url_for
from itertools import count
import json
from model import User, Product, Dish
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery

CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
API_SERVICE_NAME = 'drive'
API_VERSION = 'v2'
SECRET_KEY = os.urandom(24)

app = Flask(__name__)
app.secret_key = SECRET_KEY

def credentials_to_dict(credentials):
  return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}

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
    return render_template('search_layout.html')


@app.route('/authorize')
def authorize():
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, redirect_uri='http://127.0.0.1:5000/profiles/1')

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')

    # Store the state so the callback can verify the auth server response.
    session['state'] = state
    return redirect(authorization_url)


@app.route('/profiles/<profile>')
def profile(profile):
    credentials = google.oauth2.credentials.Credentials(
        **session['credentials'])

    drive = googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)

    files = drive.files().list().execute()
    session['credentials'] = credentials_to_dict(credentials)
    return render_template('profile.html', profile=mock_user)


@app.route('/profiles/<profile>/history')
def profile_history(profile):
    return render_template('history.html', profile=mock_user)


@app.route('/profiles/<profile>/favourites')
def profile_favourites(profile):
    return render_template('favourites.html', profile=mock_user)


@app.route('/profiles/<profile>/products')
def profile_products(profile):
    return render_template('products.html', profile=mock_user)


@app.route('/recipes')
def recipe_results():
    return render_template('recipes.html', recipes=results)


@app.route('/recipes/<recipe_id>')
def recipe_details(recipe_id):
    return render_template('recipe.html', recipe=results[int(recipe_id)])


if __name__ == '__main__':
    app.run()
