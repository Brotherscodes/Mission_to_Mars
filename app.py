# Import the needed dependencies:
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# set up instance of flask:
app = Flask(__name__)

# tell python how to connect to Mongo using PyMongo:
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Home route:
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# Scrape route:
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   return redirect('/', code=302)

# Close the Flask app:
if __name__ == "__main__":
   app.run()

# The Flask app is completed and will pull from the scraping.py file.