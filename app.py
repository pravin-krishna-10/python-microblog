import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__) 
    username = quote_plus("Pravin")
    password = quote_plus("Ias@emc22")  # Encodes '@' to '%40'

    #uri = f"mongodb+srv://{username}:{password}@microblog-application.i9io9be.mongodb.net/"
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.microblog

    entries = []

    @app.route("/", methods=["GET", "POST"])
    def home():
        print([e for e in app.db.entries.find({})])
        if request.method == "POST":
            entry_content = request.form.get("content")
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            #entries.append((entry_content, formatted_date))
            app.db.entries.insert_one({"content" : entry_content, "date":formatted_date})

        entries_with_date = [
            (
                entry["content"],
                entry["date"], 
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in app.db.entries.find({})
            
        ]
        return render_template("home.html", entries=entries_with_date)
    
    return app