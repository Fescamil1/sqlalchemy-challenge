#Imports
from flask import Flask, jsonify
import numpy as np
import pandas as pd
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import inspect

#Engines and Database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

session = Session(engine)

#Set up Flask
app = Flask(__name__)

#Setup Flask Routes
@app.route("/")
def welcome():
    return (
        f"Welcome, the available routes are:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
    )

#convert the query results into a dictionary
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Calculate the date 1 year ago from the last data point in the database
    #find the most recent date
    mostrecent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    
    #calculate the date 1 year  from the most recent date found in the db
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Query for the date and precipitation for the last year
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_date).order_by(Measurement.date).all()

    # Return JSON representation of dictionary
    precip_dict = {date: prcp for date, prcp in precipitation}
    return jsonify(precip_dict)

