from locust import HttpLocust, TaskSequence, seq_task
from itertools import count

counter1 = count()
counter2 = count()


class WebsiteTasks(TaskSequence):
    @seq_task(1)
    def add_product(self):
        self.client.post('/profile/products',
                         {'name': '{}'.format(str(next(counter1))), 'quantity': '1', 'unit': 'g'})

    @seq_task(2)
    def delete_product(self):
        self.client.post('/profile/products/delete', {'product_name': str(next(counter2))})


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    min_wait = 0
    max_wait = 10000
