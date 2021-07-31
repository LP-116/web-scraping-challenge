from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mars_file

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")

def home():

    mars_data = mongo.db.data.find_one()

    return render_template("index.html", mars=mars_data)

@app.route("/scrape")
def scrape():

    data = mars_file.scrape_all()

    mongo.db.data.update({}, data, upsert=True)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

