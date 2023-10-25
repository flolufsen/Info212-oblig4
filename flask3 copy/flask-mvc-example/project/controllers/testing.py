

from project import app
from flask import render_template, request, redirect, url_for
from project.models.my_dao import *

@app.route('/get_cars', methods=['GET']) 
def query_records():
     return findAllCars()

 # The method uses the registration number to find the car
  # object from database
@app.route('/get_cars_by_reg_number', methods=['POST'])
def find_car_by_reg_number():
    record = json.loads(request.data)
    print(record)
    print(record['reg'])
    return findCarByReg(record['reg'])



@app.route('/save_car', methods=["POST"]) 
def save_car_info():
    make = request.form["make"]
    model = request.form["model"]
    reg = request.form["reg"]
    year = request.form["year"]
    capacity = request.form["capacity"]
    return save_car(make, model, reg, year, capacity)



  # The method uses the registration number to find the car
# object from database and updates other informaiton from
# the information provided as input in the json object
@app.route('/update_car', methods=['PUT']) 
def update_car_info():
    record = json.loads(request.data)
    print(record)
    return update_car(record['make'], record['model'], 
    record['reg'], record['year'], record['capacity'])

  # The method uses the registration number to find the car
  # object from database and removes the records
@app.route('/delete_car', methods=['DELETE'])
def delete_car_info():
    record = json.loads(request.data)
    print(record)
    delete_car(record['reg'])
    return findAllCars()




#CHAT GPT

@app.route('/customer', methods=["POST"])
def create_customer_endpoint():
    name = request.form["name"]
    age = request.form["age"]
    address = request.form["address"]
    create_customer(name, age, address)
    return jsonify({"message": "Customer created!"})

@app.route('/customer', methods=["GET"])
def get_customers_endpoint():
    return jsonify(get_customers())

@app.route('/customer/<customer_id>', methods=["PUT"])
def update_customer_endpoint(customer_id):
    name = request.form["name"]
    age = request.form["age"]
    address = request.form["address"]
    update_customer(customer_id, name, age, address)
    return jsonify({"message": "Customer updated!"})

@app.route('/customer/<customer_id>', methods=["DELETE"])
def delete_customer_endpoint(customer_id):
    delete_customer(customer_id)
    return jsonify({"message": "Customer deleted!"})

@app.route('/employee', methods=["POST"])
def create_employee_endpoint():
    name = request.form["name"]
    address = request.form["address"]
    branch = request.form["branch"]
    create_employee(name, address, branch)
    return jsonify({"message": "Employee created!"})

@app.route('/employee', methods=["GET"])
def get_employees_endpoint():
    return jsonify(get_employees())

@app.route('/employee/<employee_id>', methods=["PUT"])
def update_employee_endpoint(employee_id):
    name = request.form["name"]
    address = request.form["address"]
    branch = request.form["branch"]
    update_employee(employee_id, name, address, branch)
    return jsonify({"message": "Employee updated!"})

@app.route('/employee/<employee_id>', methods=["DELETE"])
def delete_employee_endpoint(employee_id):
    delete_employee(employee_id)
    return jsonify({"message": "Employee deleted!"})
