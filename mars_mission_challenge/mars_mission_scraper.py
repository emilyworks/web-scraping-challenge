#import dependencies

from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scraper

app = Flask(__name__)


# set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_mission"
mongo = PyMongo(app)

# set up flask routes

@app.route("/")
def index():
    mars_mission = mongo.db.mars_mission.find_one()
    return render_template("index.html", mars_mission=mars_mission)


@app.route("/scrape")
def scrape():
    mars_mission = mongo.db.mars_mission
    mars_mission_data = scraper.scrape()
    mars_mission.update({}, mars_mission_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
