from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    mars_recors=mongo.db.mars_recors.find_one()

    # Return template and data
    return render_template("index.html", mars_data=mars_recors)

@app.route("/scrape")
def scraper():
    mars_recors = mongo.db.mars_recors
    mars_data = scrape_mars.scrape()
    mars_recors.update({}, mars_data, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
