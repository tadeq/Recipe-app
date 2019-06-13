from locust import HttpLocust, TaskSet, task


class WebsiteTasks(TaskSet):

    @task(1)
    def delete_product(self):
        self.client.get('/recipes?query=cheese')

    @task(1)
    def delete_product(self):
        self.client.get('/recipes?query=ham')

    @task(1)
    def delete_product(self):
        self.client.get('/recipes?query=chicken')

    @task(1)
    def delete_product(self):
        self.client.get('/recipes?query=beef')

    @task(1)
    def delete_product(self):
        self.client.get('/recipes?query=pizza')


class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    min_wait = 0
    max_wait = 10000
