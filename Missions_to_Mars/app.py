from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app=Flask(__name__)

mongo=PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    return "Hello"

@app.route("/scrape")
def scrape():
    mars=mongo.db.mars
    mars_data=scrape_mars.scrape_all()
    print(mars_data)
    return 

if __name__=="__main__":
    app.run(debug=True)