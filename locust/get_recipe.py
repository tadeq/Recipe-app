from locust import HttpLocust, TaskSequence, seq_task, task
from itertools import count
import json

counter = count()
results = None


class WebsiteTasks(TaskSequence):

    @seq_task(1)
    def add_product(self):
        global results
        response = self.client.get('/recipes?query=chicken')
        print(response.text)
        results = [hit['recipe']['uri'].replace('http://www.edamam.com/ontologies/edamam.owl#recipe_', '') for hit
                   in json.loads(response.text)['hits']]

    @seq_task(2)
    @task(100)
    def delete_product(self):
        global results
        self.client.get('/recipes/' + results[next(counter)].id)


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    min_wait = 0
    max_wait = 10000
