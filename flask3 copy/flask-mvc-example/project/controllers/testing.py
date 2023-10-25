from project import app
from flask import render_template, request, redirect, url_for
from project.models.my_dao import *
@app.route('/get_cars', methods=['GET'])

def query_records():
    return findAllCars()