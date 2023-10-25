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

# CRUD for Cars
@app.route('/create_car', methods=['POST'])
def create_car():
    data = request.json
    make = data["make"]
    model = data["model"]
    year = data["year"]
    location = data["location"]
    status = "available"
    save_car(make, model, year, location, status, car_id)
    return jsonify({"message": "Car created successfully!"})

#CRUD for customer
@app.route('/create_customer', methods=['POST'])
def create_customer():
    data = request.json
    name = data["name"]
    age = data["age"]
    address = data["address"]
    customer_id = str(uuid.uuid4())  # Generate a unique ID
    save_customer(name, age, address, customer_id)
    return jsonify({"message": "Customer created successfully!"})

#CRUD for employee
@app.route('/create_employee', methods=['POST'])
def create_employee():
    data = request.json
    name = data["name"]
    address = data["address"]
    branch = data["branch"]
    employee_id = str(uuid.uuid4())  # Generate a unique ID
    save_employee(name, address, branch, employee_id)
    return jsonify({"message": "Employee created successfully!"})
