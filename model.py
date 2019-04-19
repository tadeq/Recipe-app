diet_labels = ['balanced', 'high-protein', 'high-fiber', 'low-fat', 'low-carb', 'low-sodium', 'vegan', 'vegetarian',
               'paleo', 'dairy-free', 'gluten-free', 'wheat-free', 'fat-free', 'low-sugar',
               'egg-free', 'peanut-free', 'tree-nut-free', 'soy-free', 'fish-free', 'shellfish-free']


class Dish:
    def __init__(self, recipe):
        self.id = recipe['uri'].replace('http://www.edamam.com/ontologies/edamam.owl#recipe_', '')
        self.name = recipe['label']
        self.ingredients = ['{} ({} g)'.format(i['text'], str(round(i['weight'], 1))) for i in recipe['ingredients']]
        self.image_url = recipe['image']
        self.diet_labels = recipe['healthLabels'] + recipe['dietLabels']
        self.cuisine_type = recipe['cuisineType'] if 'cuisineType' in recipe else None
        self.calories = round(recipe['totalNutrients']['ENERC_KCAL']['quantity'], 1)
        self.carbs = round(recipe['totalNutrients']['CHOCDF']['quantity'], 1)
        self.fat = round(recipe['totalNutrients']['FAT']['quantity'], 1)
        self.protein = round(recipe['totalNutrients']['PROCNT']['quantity'], 1)
        self.time = recipe['totalTime']
        self.weight = round(recipe['totalWeight'], 0)
        self.url = recipe['url']


class Product:
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit


class HistoryEntry:
    def __init__(self, query, date_time):
        self.query = query
        self.date_time = date_time


class User:
    def __init__(self, profile_id, name, surname):
        self.id = profile_id
        self.name = name
        self.surname = surname
        self.favourites = []
        self.history = []
        self.products = []
