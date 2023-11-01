

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



# @app.route('/save_car', methods=["POST"]) 
# def save_car_info():
#     make = request.form["make"]
#     model = request.form["model"]
#     reg = request.form["reg"]
#     year = request.form["year"]
#     capacity = request.form["capacity"]
#     return save_car(make, model, reg, year, capacity)



#   # The method uses the registration number to find the car
# # object from database and updates other informaiton from
# # the information provided as input in the json object
# @app.route('/update_car', methods=['PUT']) 
# def update_car_info():
#     record = json.loads(request.data)
#     print(record)
#     return update_car(record['make'], record['model'], 
#     record['reg'], record['year'], record['capacity'])

#   # The method uses the registration number to find the car
#   # object from database and removes the records
# @app.route('/delete_car', methods=['DELETE'])
# def delete_car_info():
#     record = json.loads(request.data)
#     print(record)
#     delete_car(record['reg'])
#     return findAllCars()


# 1, 
@app.route('/save_car', methods=["POST"]) 
def save_car_info():
    make = request.form["make"]
    model = request.form["model"]
    reg = request.form["reg"]
    year = request.form["year"]
    capacity = request.form["capacity"]
    location = request.form["location"]  # Get location from the form
    status = request.form.get("status", "available")  # Get status from the form, default is available
    return save_car(make, model, reg, year, capacity, location, status)

@app.route('/update_car', methods=['PUT']) 
def update_car_info():
    record = json.loads(request.data)
    return update_car(
        record['make'], record['model'], record['reg'], 
        record['year'], record['capacity'], record['location'], record['status']
    )

#2. CRUD for "Customers"
@app.route('/save_customer', methods=["POST"]) 
def save_customer_info():
    name = request.form["name"]
    age = request.form["age"]
    address = request.form["address"]
    return save_customer(name, age, address)

@app.route('/get_all_customers', methods=['GET']) 
def get_all_customers():
    return find_all_customers()

@app.route('/get_customer_by_name', methods=['POST'])
def get_customer_by_name():
    record = json.loads(request.data)
    return find_customer_by_name(record['name'])

@app.route('/update_customer', methods=['PUT']) 
def update_customer_info():
    record = json.loads(request.data)
    name = record['name']
    age = record.get('age')
    address = record.get('address')
    return update_customer(name, age, address)

@app.route('/delete_customer', methods=['DELETE'])
def delete_customer_info():
    record = json.loads(request.data)
    delete_customer(record['name'])
    return {"message": "Customer deleted successfully!"}

#3. CRUD for "Employee" class

@app.route('/save_employee', methods=["POST"]) 
def save_employee_info():
    name = request.form["name"]
    address = request.form["address"]
    branch = request.form["branch"]
    return save_employee(name, address, branch)

@app.route('/get_all_employees', methods=['GET']) 
def get_all_employees():
    return find_all_employees()

@app.route('/get_employee_by_name', methods=['POST'])
def get_employee_by_name():
    record = json.loads(request.data)
    return find_employee_by_name(record['name'])

@app.route('/update_employee', methods=['PUT']) 
def update_employee_info():
    record = json.loads(request.data)
    name = record['name']
    address = record.get('address')
    branch = record.get('branch')
    return update_employee(name, address, branch)

@app.route('/delete_employee', methods=['DELETE'])
def delete_employee_info():
    record = json.loads(request.data)
    delete_employee(record['name'])
    return {"message": "Employee deleted successfully!"}

#4/5. Order_car implementation

@app.route('/order-car', methods=["POST"]) 
def order_car_endpoint():
    try:
        record = json.loads(request.data)
        customer_id = int(record["customer_id"])
        car_id = int(record["car_id"])
        return order_car(customer_id, car_id)
    except Exception as e:
        return {"error": str(e)}, 400

# 6. Cancel_order_car endpoint
@app.route('/cancel-order-car', methods=["POST"]) 
def cancel_order_car_endpoint():
    try:
        record = json.loads(request.data)
        customer_id = int(record["customer_id"])
        car_id = int(record["car_id"])
        return cancel_order_car(customer_id, car_id)
    except Exception as e:
        return {"error": str(e)}, 400

#7. rent-car function

@app.route('/rent-car', methods=["POST"]) 
def rent_car_endpoint():
    try:
        record = json.loads(request.data)
        customer_id = int(record["customer_id"])
        car_id = int(record["car_id"])
        return rent_car(customer_id, car_id)
    except Exception as e:
        return {"error": str(e)}, 400

# 8. Return-car function

@app.route('/return-car', methods=["POST"]) 
def return_car_endpoint():
    try:
        record = json.loads(request.data)
        customer_id = int(record["customer_id"])
        car_id = int(record["car_id"])
        return_status = record["status"]
        return return_car(customer_id, car_id, return_status)
    except Exception as e:
        return {"error": str(e)}, 400
