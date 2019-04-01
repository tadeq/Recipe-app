import requests
from pprint import pprint
import json

if __name__ == '__main__':
    # with open('auth.txt') as auth_file:
    #     app_id = auth_file.readline().strip()
    #     app_key = auth_file.readline().strip()
    #
    # response = requests.get(
    #     'https://api.edamam.com/search?q=chicken&app_id={}&app_key={}'.format(app_id, app_key))
    #
    # f = open('response.json', 'w+')
    # json.dump(response.json(), f)
    # f.close()

    with open('response.json') as res_file:
        response = json.load(res_file)

    hits = response['hits']
    recipe = hits[2]['recipe']
    pprint(recipe)
    energy = recipe['totalNutrients']['ENERC_KCAL']
    carbs = recipe['totalNutrients']['CHOCDF']
    fat = recipe['totalNutrients']['FAT']
    protein = recipe['totalNutrients']['PROCNT']
    print(energy, carbs, fat, protein)
