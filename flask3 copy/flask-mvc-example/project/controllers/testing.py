

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

#Endpoint ordering a car
@app.route('/order-car', methods=['POST'])
def order_car():
    data = request.json
    customer_id = data['customer_id']
    car_id = data['car_id']

    # Check if the customer has not booked other cars.
    booked_car = find_booked_car_for_customer(customer_id)
    if booked_car:
        return jsonify({"error": "Customer already has a booking!"}), 400

    # Change the status of the car to 'booked'
    book_car_for_customer(customer_id, car_id)
    return jsonify({"message": "Car booked successfully!"})

#Endpoint cancel order
@app.route('/cancel-order-car', methods=['POST'])
def cancel_order_car():
    data = request.json
    customer_id = data['customer_id']
    car_id = data['car_id']

    # Check if the customer has booked the specific car.
    booked_car = find_specific_booked_car_for_customer(customer_id, car_id)
    if not booked_car:
        return jsonify({"error": "No booking found for this customer and car!"}), 400

    # Cancel the booking
    cancel_booking_for_car_and_customer(customer_id, car_id)
    return jsonify({"message": "Booking canceled successfully!"})


