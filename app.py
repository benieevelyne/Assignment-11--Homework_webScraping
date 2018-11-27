from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    print(mars)
    return render_template("index.html",mars_info=mars)


@app.route("/scrape")
def scraper():
 # Run scrapped functions
    mars_info = mongo.db.mars
    mars_news = scrape_mars.scrape_mars_news()
    mars_image = scrape_mars.scrape_mars_image()
    mars_facts = scrape_mars.scrape_mars_facts()
    mars_weather = scrape_mars.scrape_mars_weather()
    mars_hemispheres = scrape_mars.scrape_mars_hemispheres()
    
    mars_data = mars_news
    mars_data.update(mars_image)
    mars_data.update(mars_facts)
    mars_data.update(mars_weather)
    mars_data.update(mars_hemispheres)



    mars_info.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
  #  scraper()
    app.run(debug=True)



    