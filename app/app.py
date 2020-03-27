import os
from flask import (
        Flask,
        render_template,
        request)
from flask_sqlalchemy import SQLAlchemy
from api import corona
from datetime import datetime
import mail_sender
import re

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

project_directory = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_directory, "coronavirusinfo.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

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
    app.run()
