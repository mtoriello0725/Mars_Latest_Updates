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


def scrape():

	# Run scraped functions
	news = scrape.latest_marts_news()

	# store results in dictionary:
	mars = {
		"title":news.title,
		"description":news.description
	}

	# insert into Mongo
	mongo.db.collection.insert_one(mars)

	# Redirect to home page
	return redirect("/", code=302)


# If this script is the main application, run app.
if __name__ == "__main__":
	app.run(debug=True)