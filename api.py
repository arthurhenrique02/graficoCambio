from flask import Flask, request, jsonify, render_template
from flask_restful import Api, Resource
from datetime import date, timedelta

import sqlite3
import os
import requests
import json

# create app and api
app = Flask(__name__)
api = Api(app)

# get current directory
current_d = os.path.dirname(os.path.abspath(__file__))

# db location
DB_LOCATION = "/api_db.db"

# API URL
URL_API = "https://api.frankfurter.app/"

# connect db and check some things when program run
with  sqlite3.connect(current_d + DB_LOCATION) as db:

    # create an cursor
    c = db.cursor()

    # get past dates
    past_dates = [date.today() - timedelta(days=x) for x in range(30)]

    # add a month exchange rate if db is empty
    if len(list(c.execute("SELECT * FROM latests"))) <= 0:
        for past_date in past_dates:
            # get api response in json format
            API_response = requests.get(URL_API + str(past_date)).json()

            # query to insert into db
            c.execute("INSERT INTO latests(amount, base, date, rates) VALUES (?, ?, ?, ?)", (API_response["amount"], str(API_response["base"]), str(past_date), str(API_response["rates"]),),)

            # commit changes
            db.commit()

    # check if have 30 days data // already check if have today`s data
    # check what`s missing date
    for past_date in past_dates:
        if len(list(c.execute("SELECT * FROM latests WHERE date = ?", (str(past_date),),))) <= 0:
            # get date info
            API_response = requests.get(URL_API + str(past_date)).json()

            # add info into db
            c.execute("INSERT INTO latests(amount, base, date, rates) VALUES (?, ?, ?, ?)", (API_response["amount"], str(API_response["base"]), str(past_date), str(API_response["rates"]),),)

            # commit changes
            db.commit()

# Define API
class TakeExchangeInfo(Resource):
    # api get method 
    def get(self, currencie_name="USD", total_days=7): # set default currencie and days values  
        # list to return items
        db_items = []

        print(currencie_name, total_days)
        # connect db
        with sqlite3.connect(current_d + DB_LOCATION) as db:
            # create cursor
            c = db.cursor()

            # grab db response 
            result = list(c.execute("SELECT * FROM latests ORDER BY date DESC LIMIT ?", (int(total_days),),).fetchall())

            # turn db data into a dict 
            for item in result:
                # create dict items
                resource_fields = {
                    "id": item[0],
                    "amount": item[1],
                    "base": item[2],
                    "date": item[3],
                    "currencie": currencie_name,
                    "rates": round(eval(item[4])[currencie_name], 2), # create a new dict inside rates using eval
                } 
                # append dict into a list
                db_items.append(resource_fields)

            # return a json content of data 
            return jsonify({"exchanges": db_items})

    def post(self, currencie_name="USD", total_days=7):
        # list to return items
        db_items = []

        print(currencie_name, total_days)
        # connect db
        with sqlite3.connect(current_d + DB_LOCATION) as db:
            # create cursor
            c = db.cursor()

            # grab db response 
            result = list(c.execute("SELECT * FROM latests ORDER BY date DESC LIMIT ?", (int(total_days),),).fetchall())

            # turn db data into a dict 
            for item in result:
                # create dict items
                resource_fields = {
                    "id": item[0],
                    "amount": item[1],
                    "base": item[2],
                    "date": item[3],
                    "currencie": currencie_name,
                    "rates": round(eval(item[4])[currencie_name], 2), # create a new dict inside rates using eval
                } 
                # append dict into a list
                db_items.append(resource_fields)

            # return a json content of data 
            return jsonify({"exchanges": db_items})

# add route resource
api.add_resource(TakeExchangeInfo, "/exchanges/<string:currencie_name>/<int:total_days>")

# create route to test
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        return TakeExchangeInfo
    
    
    with sqlite3.connect(current_d + DB_LOCATION) as db:
        # create cursor
        c = db.cursor()

        # grab db response 
        result = list(c.execute("SELECT * FROM latests LIMIT 1").fetchall())

        currencies = [currencie for currencie in eval(result[0][4])]
        return render_template("index.html", currencies=currencies)

# run
if __name__ == "__main__":
    app.run(debug=True)
