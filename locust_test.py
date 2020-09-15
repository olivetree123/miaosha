import os
import json
from locust import HttpUser, TaskSet, task, between

# class WebsiteTasks(TaskSet):
#     def on_start(self):
#         self.client.post("/api/login",
#                          json={
#                              "account": "gaojian",
#                              "cipher": "123456"
#                          })

#     @task
#     def buy(self):
#         r = self.client.post("/api/buy",
#                              json={
#                                  "goods": [{
#                                      "id": "b9c661c3c5d949ca866512c936bcb6f1",
#                                      "amount": 1,
#                                  }]
#                              })
#         if r.status_code == 200:
#             rst = json.loads(r.text, strict=False)
#             if rst["code"] == 0:
#                 r.success()
#             else:
#                 r.failure("code：%s ErrorMsg：%s" %
#                           (rst["code"], rst["message"]))
#         else:
#             r.failure("status_code：%s" % r.status_code)


class WebsiteUser(HttpUser):
    # task_set = WebsiteTasks
    host = "http://localhost:5000"
    wait_time = between(1, 2)
    token = "ea0d85e817874df9a45c1606de2970eb"

    # def on_start(self):
    #     r = self.client.post("/api/login",
    #                          json={
    #                              "account": "gaojian",
    #                              "cipher": "123456"
    #                          })
    #     if not r.ok:
    #         raise Exception("failed to login")
    #     rst = json.loads(r.text, strict=False)
    #     if rst["code"] != 0:
    #         raise Exception("failed to login")
    #     self.token = rst["data"]["token"]

    @task
    def buy(self):
        r = self.client.post(
            "/api/buy",
            headers={"Authorization": "Token {}".format(self.token)},
            json={
                "goods": [{
                    "id": "b9c661c3c5d949ca866512c936bcb6f1",
                    "amount": 1,
                }]
            })
        if r.status_code == 200:
            rst = json.loads(r.text, strict=False)
            if rst["code"] != 0:
                print("Error, code = %s, ErrorMsg = %s" %
                      (rst["code"], rst["message"]))
        else:
            print("Request Failed, status_code = ", r.status_code)
