from locust import HttpUser, task

class Api(HttpUser):
    @task
    def api(self):
        self.client.get("/")
        self.client.get("/api/hello")