import os
from flask import (
        Flask,
        render_template,
        request)
from flask_sqlalchemy import SQLAlchemy
from api import corona
from datetime import datetime
import mail_sender
import re, json
import requests as request_lib
from flask_cors import CORS, cross_origin

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

project_directory = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_directory, "coronavirusinfo.db"))

app = Flask(__name__)
CORS(app, support_credentials=True)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

@app.route('/get_corona')
@cross_origin(supports_credentials=True)
def get_corona_data():
    country = request.args.get("country")
    response = request_lib.get("https://services1.arcgis.com/0MSEUqKaxRlEPj5g/arcgis/rest/services/ncov_cases/FeatureServer/2/query?f=json&where=\
        Country_Region%3D%27{}%27&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&resultOffset=0&resultRecordCount=50&cacheHint=true".format(country))

    dict_data = json.loads(response.text)

    for info in dict_data.get("features"):
        result = info.get("attributes")
    
    return result

@app.route("/", methods=["GET", "POST"])
def hello():
    email = ""
    if request.form:
        country = request.form.get("country")
        email = request.form.get("email")
        data = corona.get_information(country)

        info = CoronaInfo(
                last_record=datetime.now(),
                country=data.get("Country_Region"),
                deaths=data.get("Deaths"),
                recovered=data.get("Recovered"),
                active=data.get("Active"),
                confirmed=data.get("Confirmed")
            )
        db.session.add(info)
        db.session.commit()

    if email and EMAIL_REGEX.match(email):
        print("Mail validation is pass for {}.".format(email))
        corona.write_to_file(str(data))
        mail_sender.main([email])

    coronainf = CoronaInfo.query.all()
    
    return render_template("home.html", coronainf=coronainf)


class CoronaInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_record = db.Column(db.DateTime, nullable=False)
    country = db.Column(db.String(80), nullable=False)
    deaths = db.Column(db.String(80), nullable=False)
    recovered = db.Column(db.String(80), nullable=False)
    active = db.Column(db.String(80), nullable=False)
    confirmed = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return "<Country: {}, Deaths: {}, Recovered: {}, Active: {}, Confirmed: {}>".format(self.country, self.deaths, self.recovered, self.active, self.confirmed)

if __name__ == "__main__":
    db.create_all()
    app.run()
