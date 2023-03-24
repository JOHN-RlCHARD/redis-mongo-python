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

# INSERCAO DOS DADOS NO MONGO
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

def removeData(cpf):
    query = {
        "cpf": str(cpf)
    }
    collection.delete_one(query)
    redisconn.delete(str(cpf))

# UNCOMMENT TO INSERT DATA IN MONGODB
#insertData(1)

removeData(35310192310)

def main():
    opt = "10"
    while opt != "0":
        print("\nType desired option:")
        print("[1] - Insert data")
        print("[2] - Delete data\n")
        print("[0] - Quit")
        opt = input()
        match opt:
            case "1":
                print("Type number of random data to insert: ")
                insertData(int(input()))
            case "2":
                print("Type cpf of the person to remove: ")
                removeData(input())
            case "0":
                break
            case _:
                print("Invalid option.")

main()