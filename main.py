import random
import pandas as pd
import json
import pymongo
from pymongo import MongoClient
from redisconn import RedisConnection

# CONEXAO COM BD
print("User password: ")
password = input()
client = pymongo.MongoClient("mongodb+srv://joaoensenat:"+password+"@cluster0.3ijz94k.mongodb.net/?retryWrites=true&w=majority")
db = client['redis']
collection = db['students']

# CONEXAO REDIS
redisconn = RedisConnection()

# LEITURA DOS DADOS DO EXCEL
data = pd.read_excel(r'C:\Users\jre10\OneDrive\Documentos\Codes\trabredis\dados.xlsx')
names = data["Nome"].values.tolist()
lastNames = data["Sobrenome"].values.tolist()
courses = data["Cursos"].values.tolist()

class Person:
    def __init__(self, name, cpf, course, year):
        self.name = name
        self.cpf = cpf
        self.course = course
        self.year = year
    def __str__(self):
        return self.name+" "+self.cpf+" "+self.course+" "+self.year

# GERAR CPF
def generateCpf():
    cpf = ""
    for i in range(11):
        cpf = cpf+str(random.randint(0,9))
    return cpf

# GERAR PESSOA ALEATORIA
def generateRandomPerson():
    randomPerson = Person(
        names[random.randint(0,len(names)-1)]+" "+lastNames[random.randint(0,len(lastNames)-1)],
        generateCpf(),
        courses[random.randint(0,len(courses)-1)],
        str(random.randint(2010,2023)))
    return randomPerson

# INSERCAO DOS DADOS NO MONGO E REDIS
def insertData(qtd):
    for i in range(qtd):

        newPerson = generateRandomPerson()

        personjson = {
            "nome": newPerson.name,
            "cpf": newPerson.cpf,
            "curso_aprovado": newPerson.course,
            "ano": newPerson.year
            }
        y = json.dumps(personjson)
        # INSERT IN MONGO
        collection.insert_one(personjson)
        # INSERT IN REDIS
        redisconn.insert(y)

        print("["+str(i+1)+"] Inserted: "+str(newPerson))

# REMOVER DADO NO MONGO E REDIS
def removeData(cpf):
    query = {
        "cpf": str(cpf)
    }
    collection.delete_one(query)
    redisconn.delete(str(cpf))

# INSERIR 5000 DADOS APENAS NO MONGO
def insert5000():
    for i in range(5000):
        newPerson = generateRandomPerson()

        personjson = {
            "nome": newPerson.name,
            "cpf": newPerson.cpf,
            "curso_aprovado": newPerson.course,
            "ano": newPerson.year
            }
        collection.insert_one(personjson)
        print("["+str(i+1)+"] Inserted: "+str(newPerson))

# ATUALIZAR TODOS OS DADOS DO MONGO PARA O REDIS
def insertAllInRedis():
    cursor = collection.find({})
    for document in cursor:
        personjson = {
            "nome": document["nome"],
            "cpf": document["cpf"],
            "curso_aprovado": document["curso_aprovado"],
            "ano": document["ano"]
        }
        jsonDoc = json.dumps(personjson)
        redisconn.insert(jsonDoc)

def main():
    opt = "10"
    while opt != "0":
        print("\nType desired option:")
        print("[1] - Insert data(Simultaneously in Mongo and Redis)")
        print("[2] - Delete data(Simultaneously in Mongo and Redis)")
        print("[3] - Insert 5000 only in Mongo")
        print("[4] - Update all data in Redis")
        print("[0] - Quit\n")
        opt = input()
        match opt:
            case "1":
                print("Type number of random data to insert: ")
                insertData(int(input()))
            case "2":
                print("Type cpf of the person to remove: ")
                removeData(input())
            case "3":
                insert5000()
            case "4":
                insertAllInRedis()
            case "0":
                break
            case _:
                print("Invalid option.")

main()