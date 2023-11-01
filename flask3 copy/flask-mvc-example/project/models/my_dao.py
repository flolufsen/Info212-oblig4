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


 
#1. CRUD for "Cars" class  
#We have added status to the function
def save_car(make, model, reg, year, capacity):
  cars = _get_connection().execute_query(
          "MERGE (a:Car{make: $make, model: $model, reg: $reg, year: $year, capacity: $capacity, location: $location, status: $status}) RETURN a;",
          make=make, model=model, reg=reg, year=year, capacity=capacity, location=location, status=status)
      
  nodes_json = [node_to_json(record["a"]) for record in cars]
  return nodes_json

def delete_car(reg):
  _get_connection().execute_query("MATCH (a:Car{reg: $reg}) delete a;", reg = reg)

#
def update_car(make, model, reg, year, capacity, location, status):
  with _get_connection().session() as session:
      car = session.run(
            """
            MATCH (a:Car{reg: $reg}) 
            SET a.make = $make, a.model = $model, a.year = $year, a.capacity = $capacity, a.location = $location, a.status = $status
            RETURN a;
            """,
            make=make, model=model, reg=reg, year=year, capacity=capacity, location=location, status=status
        )
      nodes_json = [node_to_json(record["a"]) for record in car]
      return nodes_json


#2. CRUD for "Customer" class
def save_customer(name, age, address):
    with _get_connection().session() as session:
        customers = session.run(
            """
            MERGE (c:Customer{name: $name, age: $age, address: $address})
            RETURN c;
            """,
            name=name, age=age, address=address
        )
        nodes_json = [node_to_json(record["c"]) for record in customers]
        return nodes_json

def find_all_customers():
    with _get_connection().session() as session:
        customers = session.run("MATCH (c:Customer) RETURN c;")
        nodes_json = [node_to_json(record["c"]) for record in customers]
        return nodes_json

def find_customer_by_name(name):
    with _get_connection().session() as session:
        customers = session.run("MATCH (c:Customer) WHERE c.name = $name RETURN c;", name=name)
        nodes_json = [node_to_json(record["c"]) for record in customers]
        return nodes_json

def update_customer(name, age=None, address=None):
    with _get_connection().session() as session:
        query = "MATCH (c:Customer{name: $name}) "
        if age:
            query += "SET c.age = $age "
        if address:
            query += "SET c.address = $address "
        query += "RETURN c;"
        customer = session.run(query, name=name, age=age, address=address)
        nodes_json = [node_to_json(record["c"]) for record in customer]
        return nodes_json

def delete_customer(name):
    with _get_connection().session() as session:
        session.run("MATCH (c:Customer{name: $name}) DELETE c;", name=name)

#3. CRUD for "Employee" class
def save_employee(name, address, branch):
    with _get_connection().session() as session:
        employees = session.run(
            """
            MERGE (e:Employee{name: $name, address: $address, branch: $branch})
            RETURN e;
            """,
            name=name, address=address, branch=branch
        )
        nodes_json = [node_to_json(record["e"]) for record in employees]
        return nodes_json

def find_all_employees():
    with _get_connection().session() as session:
        employees = session.run("MATCH (e:Employee) RETURN e;")
        nodes_json = [node_to_json(record["e"]) for record in employees]
        return nodes_json

def find_employee_by_name(name):
    with _get_connection().session() as session:
        employees = session.run("MATCH (e:Employee) WHERE e.name = $name RETURN e;", name=name)
        nodes_json = [node_to_json(record["e"]) for record in employees]
        return nodes_json

def update_employee(name, address=None, branch=None):
    with _get_connection().session() as session:
        query = "MATCH (e:Employee{name: $name}) "
        if address:
            query += "SET e.address = $address "
        if branch:
            query += "SET e.branch = $branch "
        query += "RETURN e;"
        employee = session.run(query, name=name, address=address, branch=branch)
        nodes_json = [node_to_json(record["e"]) for record in employee]
        return nodes_json

def delete_employee(name):
    with _get_connection().session() as session:
        session.run("MATCH (e:Employee{name: $name}) DELETE e;", name=name)


#4/5. Order_car implementation and checking whether the customer already has rented a car

def order_car(customer_id, car_id):
    with _get_connection().session() as session:
        # Check if the car is already rented or booked
        rented_or_booked_car = session.run(
            "MATCH (c:Car) WHERE ID(c) = $car_id AND (c.status = 'booked' OR EXISTS((:Customer)-[:RENTS]->(c))) RETURN c",
            car_id=car_id
        ).single()
        if rented_or_booked_car:
            raise Exception("Car is already rented or booked!")
        
        # Check if the customer already has a rented or booked car
        customer_car = session.run(
            "MATCH (c:Customer) WHERE ID(c) = $customer_id AND EXISTS((c)-[:RENTS]->(:Car)) RETURN c",
            customer_id=customer_id
        ).single()
        if customer_car:
            raise Exception("Customer already has a rented or booked car!")
        
        # Create the RENTS relationship and update the car status
        result = session.run(
            """
            MATCH (c:Customer), (a:Car)
            WHERE ID(c) = $customer_id AND ID(a) = $car_id
            CREATE (c)-[:RENTS]->(a)
            SET a.status = 'booked'
            RETURN a;
            """,
            customer_id=customer_id, car_id=car_id
        )
        
        nodes_json = [node_to_json(record["a"]) for record in result]
        return nodes_json

# 6. Cancel_order_car endpoint

def cancel_order_car(customer_id, car_id):
    with _get_connection().session() as session:
        # Check if the customer has booked this car
        booking_exists = session.run(
            "MATCH (c:Customer)-[r:RENTS]->(a:Car) WHERE ID(c) = $customer_id AND ID(a) = $car_id RETURN r",
            customer_id=customer_id, car_id=car_id
        ).single()

        if not booking_exists:
            raise Exception("No booking found for this customer with this car!")

        # Remove the RENTS relationship and update the car status
        result = session.run(
            """
            MATCH (c:Customer)-[r:RENTS]->(a:Car)
            WHERE ID(c) = $customer_id AND ID(a) = $car_id
            DELETE r
            SET a.status = 'available'
            RETURN a;
            """,
            customer_id=customer_id, car_id=car_id
        )
        
        nodes_json = [node_to_json(record["a"]) for record in result]
        return nodes_json

#7. rent-car function

def rent_car(customer_id, car_id):
    with _get_connection().session() as session:
        # Check if the customer has booked this car and it's in 'booked' status
        booking_exists = session.run(
            "MATCH (c:Customer)-[:RENTS]->(a:Car) WHERE ID(c) = $customer_id AND ID(a) = $car_id AND a.status = 'booked' RETURN a",
            customer_id=customer_id, car_id=car_id
        ).single()

        if not booking_exists:
            raise Exception("No valid booking found for this customer with this car!")

        # Update the car status to 'rented'
        result = session.run(
            """
            MATCH (c:Customer)-[:RENTS]->(a:Car)
            WHERE ID(c) = $customer_id AND ID(a) = $car_id
            SET a.status = 'rented'
            RETURN a;
            """,
            customer_id=customer_id, car_id=car_id
        )
        
        nodes_json = [node_to_json(record["a"]) for record in result]
        return nodes_json

# 8. Return-car function

def return_car(customer_id, car_id, return_status):
    with _get_connection().session() as session:
        # Validate the return_status
        if return_status not in ['available', 'damaged']:
            raise ValueError("Invalid return status provided!")

        # Check if the customer has rented this car and it's in 'rented' status
        renting_exists = session.run(
            "MATCH (c:Customer)-[:RENTS]->(a:Car) WHERE ID(c) = $customer_id AND ID(a) = $car_id AND a.status = 'rented' RETURN a",
            customer_id=customer_id, car_id=car_id
        ).single()

        if not renting_exists:
            raise Exception("No valid renting found for this customer with this car!")

        # Update the car status based on the return_status
        result = session.run(
            """
            MATCH (c:Customer)-[:RENTS]->(a:Car)
            WHERE ID(c) = $customer_id AND ID(a) = $car_id
            SET a.status = $return_status
            DELETE (c)-[:RENTS]->(a)
            RETURN a;
            """,
            customer_id=customer_id, car_id=car_id, return_status=return_status
        )
        
        nodes_json = [node_to_json(record["a"]) for record in result]
        return nodes_json

#KJØR KODENE I POSTMAN OG OM ALT ER RIKTIG TRENGER VI BARE Å LAGE REPORT