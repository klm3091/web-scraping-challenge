from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

@app.route("/")
def home(): 

    mars_info = mongo.db.collection.find_one()

    return render_template("index.html", mars_info=mars_info)

@app.route("/scrape")
def scrape(): 

    martian_data = scrape_mars.scrape_all()

    '''
    mars_data = scrape_mars.scrape_mars_news()
    mars_data = scrape_mars.scrape_mars_image()
    mars_data = scrape_mars.scrape_mars_facts()
    mars_data = scrape_mars.scrape_mars_weather()
    mars_data = scrape_mars.scrape_mars_hemispheres()'''
    mongo.db.collection.update({}, martian_data, upsert=True)
    #mars_info.update({}, mars_data, upsert=True)

    return redirect("/")

if __name__ == "__main__": 
    app.run(debug= True)