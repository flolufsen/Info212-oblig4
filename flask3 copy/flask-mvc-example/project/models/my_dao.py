from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
import json

URI = "neo4j+s://3d029092.databases.neo4j.io"
AUTH = ("neo4j", "vjuQ1pzfXG4vLjo9NlJDtCLTHxhrJothEVGd3T0getM")

def _get_connection() -> Driver:
   driver = GraphDatabase.driver(URI, auth=AUTH)
   driver.verify_connectivity()
   return driver

def node_to_json(node):
  node_properties = dict(node.items())
  return node_properties

def findAllCars():
  with _get_connection().session() as session:
     cars = session.run("MATCH (a:Car) RETURN a;")
     nodes_json = [node_to_json(record["a"]) for record in cars]
     print(nodes_json)
     return nodes_json

def findCarByReg(reg):
  with _get_connection().session() as session:
     cars = session.run("MATCH (a:Car) where a.reg=$reg RETURN a;", reg=reg)
     print(cars)
     nodes_json = [node_to_json(record["a"]) for record in cars]
     print(nodes_json)
     return nodes_json
  
def save_car(make, model, reg, year, capacity):
    cars = _get_connection().execute_query("MERGE (a:Car{make: $make, model: $model,reg: $reg, year: $year, capacity:$capacity}) RETURN a;", make = make, model = model, reg = reg, year = year, capacity = capacity)
    nodes_json = [node_to_json(record["a"]) for record in cars]
    print(nodes_json)
    return nodes_json

def delete_car(reg):
  _get_connection().execute_query("MATCH (a:Car{reg: $reg}) delete a;", reg = reg)






#CHATGPT

def create_customer(name, age, address):
    with _get_connection().session() as session:
        session.run("CREATE (:Customer {name: $name, age: $age, address: $address})", name=name, age=age, address=address)

def get_customers():
    with _get_connection().session() as session:
        return [node_to_json(record["a"]) for record in session.run("MATCH (a:Customer) RETURN a")]

def update_customer(customer_id, name, age, address):
    with _get_connection().session() as session:
        session.run("MATCH (a:Customer) WHERE id(a) = $id SET a.name = $name, a.age = $age, a.address = $address", id=customer_id, name=name, age=age, address=address)

def delete_customer(customer_id):
    with _get_connection().session() as session:
        session.run("MATCH (a:Customer) WHERE id(a) = $id DELETE a", id=customer_id)

def create_employee(name, address, branch):
    with _get_connection().session() as session:
        session.run("CREATE (:Employee {name: $name, address: $address, branch: $branch})", name=name, address=address, branch=branch)

def get_employees():
    with _get_connection().session() as session:
        return [node_to_json(record["a"]) for record in session.run("MATCH (a:Employee) RETURN a")]

def update_employee(employee_id, name, address, branch):
    with _get_connection().session() as session:
        session.run("MATCH (a:Employee) WHERE id(a) = $id SET a.name = $name, a.address = $address, a.branch = $branch", id=employee_id, name=name, address=address, branch=branch)

def delete_employee(employee_id):
    with _get_connection().session() as session:
        session.run("MATCH (a:Employee) WHERE id(a) = $id DELETE a", id=employee_id)