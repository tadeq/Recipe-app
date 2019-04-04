import requests
import json
from itertools import count
from pprint import pprint
from model import Dish

if __name__ == '__main__':
    # with open('auth.txt') as auth_file:
    #     app_id = auth_file.readline().strip()
    #     app_key = auth_file.readline().strip()
    #
    # response = requests.get(
    #     'https://api.edamam.com/search?q=chicken&to=100&app_id={}&app_key={}'.format(app_id, app_key))
    #
    # f = open('response.json', 'w+')
    # json.dump(response.json(), f)
    # f.close()

    with open('response.json') as res_file:
        response = json.load(res_file)

    counter = count()

    # pprint(response)
    results = [Dish(next(counter), hit['recipe']) for hit in response['hits']]
    for res in results:
        print(res.name)
