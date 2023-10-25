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



