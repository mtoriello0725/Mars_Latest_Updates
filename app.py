from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape

# Create instance of Flask application
# When program is running, __name__ will be __main__.
app = Flask(__name__)

# Configure MongoDB to application
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)




@app.route("/")
def home():

	# find data
	mars = mongo.db.collection.find()

	# return template and data
	return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape_data():

	# drop existing data in mongo
	mongo.db.collection.drop()

	# Run scraped functions
	news = scrape.latest_mars_news()
	image_url = scrape.jpl_mars_image()
	mars_weather = scrape.mars_weather()
	mars_facts = scrape.mars_facts()
	mars_hemispheres = scrape.mars_hemispheres()

	# store results in dictionary:
	mars = {
		"title":news["title"],
		"description":news["description"],
		"image_url":image_url,
		"mars_weather":mars_weather,
		"mars_facts":mars_facts,
		"mars_hemi1_title":mars_hemispheres[0]["title"],
		"mars_hemi1_img":mars_hemispheres[0]["image_url"],
		"mars_hemi2_title":mars_hemispheres[1]["title"],
		"mars_hemi2_img":mars_hemispheres[1]["image_url"],
		"mars_hemi3_title":mars_hemispheres[2]["title"],
		"mars_hemi3_img":mars_hemispheres[2]["image_url"],
		"mars_hemi4_title":mars_hemispheres[3]["title"],
		"mars_hemi4_img":mars_hemispheres[3]["image_url"]		
	}

	# insert into Mongo
	mongo.db.collection.insert_one(mars)

	# Redirect to home page
	return redirect("/", code=302)


# If this script is the main application, run app.
if __name__ == "__main__":
	app.run(debug=True)