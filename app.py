# This is the app used to run the scrape functions.

from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_scrape


# Create an instance of Flask.
app = Flask(__name__)

# Using PyMongo to establish Mongo connection.
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# This is the route to render index.html template using the data from mongo.
# Finds one record from the database and returns the template and data.
@app.route("/")
def home():

    mars_data = mongo.db.data.find_one()

    return render_template("index.html", mars=mars_data)


# This is the route that will run the scrape_all function in the mars_scrape file.
@app.route("/scrape")
def scrape():

    get_data = mars_scrape.scrape_all()

    mongo.db.data.update({}, get_data, upsert=True)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

