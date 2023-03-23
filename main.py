import random
import pandas as pd
import json
import pymongo
from pymongo import MongoClient

# CONEXAO COM BD
client = pymongo.MongoClient("mongodb+srv://joaoensenat:123abc@cluster0.3ijz94k.mongodb.net/?retryWrites=true&w=majority")
db = client['redis']
collection = db['students']

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
def insertData():
    for i in range(5000):

        newPerson = generateRandomPerson()

        collection.insert_one({
        "nome": newPerson.name,
        "cpf": newPerson.cpf,
        "curso_aprovado": newPerson.course,
        "ano": newPerson.year
        })

        print("Inserted: "+str(newPerson))

# UNCOMMENT TO INSERT DATA IN MONGODB
# insertData()