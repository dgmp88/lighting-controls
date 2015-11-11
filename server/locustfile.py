from locust import HttpLocust, TaskSet, task

# Run with: locust --host=http://localhost:8888

# We need to respond perhaps 5 times a second, check that's doable.

class UserBehavior(TaskSet):
    @task
    def index(self):
        print self.client.get("/changed/").content

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=99
    max_wait=100