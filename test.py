import requests
import json
from db_connectivity import DbConnection
from model import User, Product, Dish, HistoryEntry, diet_labels

if __name__ == '__main__':
    with open('response.json') as res_file:
        response = json.load(res_file)

    results = [Dish(hit['recipe']) for hit in response['hits']]
    print(results[0].id)
    mock_user = User(1, 'Test', 'User')
    mock_products = [Product('Chicken', 2, 'kg'), Product('Butter', 200, 'g')]
    mock_user.products = mock_products

    db = DbConnection()
    # db.create_user(mock_user)
    db.create_dish(mock_user.id, results[0])
    db.create_dish(mock_user.id, results[1])
    db.create_product(mock_user.id, mock_products[0])
    db.create_product(mock_user.id, mock_products[1])

    print(db.get_dishes_by_user(mock_user.id))
    print(db.get_products_by_user(mock_user.id))
    # print(db.get_user_by_id(mock_user.id))

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
