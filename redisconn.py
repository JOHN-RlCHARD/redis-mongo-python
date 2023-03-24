import redis
from redis.commands.json.path import Path
import json

class RedisConnection:
    def __init__(self):
        self.client = redis.Redis(host='localhost', port=6379, db=0)

    def insert(self, personjson):
        json_dict = json.loads(personjson)

        self.client.set(str(json_dict['cpf']), personjson)

        result = self.client.get(str(json_dict['cpf']))
        print(result)

    def delete(self, cpf):
        self.client.delete(cpf)


