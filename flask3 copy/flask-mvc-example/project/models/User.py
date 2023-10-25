from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
import re

URI = "neo4j+s://3d029092.databases.neo4j.io"
AUTH = ("neo4j", "vjuQ1pzfXG4vLjo9NlJDtCLTHxhrJothEVGd3T0getM")

def _get_connection() -> Driver:
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()

    return driver

def findUserByName(name):
    data = _get_connection().execute_query("MATCH (a:User) where a.name = $name RETURN a;", name=name)
    if len(data[0]) > 0:
        user = Customer(name, data[0][0][0]['age'])
        return user
    else:
        return Customer(name, "Not found in DB")

class Customer:
    def __init__(self, name, age, address):
        self.name = name
        self.age = age
        self.address = address

    def get_Name(self):
        return self.name

    def set_Name(self, value):
        self.name = value

    def get_Age(self):
        return self.age

    def set_Age(self, value):
        self.email = value
    
    def get_Address(self):
        return self.address

    def set_Address(self, value):
        self.address = value

class Car:
    def __init__(self, make, model, year, location, status):
        self.make = make
        self.model = model
        self.year = year
        self.location = location
        self.status = status

    def get_Make(self):
        return self.make

    def set_Make(self, value):
        self.make = value

    def get_Model(self):
        return self.model

    def set_Model(self, value):
        self.model = value
    
    def get_Year(self):
        return self.year

    def set_Year(self, value):
        self.year = value

    def get_Locatiion(self):
        return self.location

    def set_Location(self, value):
        self.location = value

    def get_Status(self):
        return self.status

    def set_Status(self, value):
        self.status = value
