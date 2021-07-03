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

#Convert the precipiation query results to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    # Calculate the date 1 year ago from the last data point in the database
    #find the most recent date
    mostrecent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    
    #calculate the date 1 year  from the most recent date found in the db
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # Query for the date and precipitation for the last year
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_date).order_by(Measurement.date).all()

    session.close()

    # Return JSON representation of dictionary
    precip_dict = {date: prcp for date, prcp in precipitation}
    return jsonify(precip_dict)



#Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    #list of stations from the dataset.
    station_results=session.query(Station.id,Station.station,Station.name,Station.latitude,Station.longitude,Station.elevation).all()

    session.close()

    # Return JSON representation of dictionary

    stations = []
    for id, station,name,lat,lon,el in station_results:
        station_dict = {}
        station_dict["ID"] = id
        station_dict["Station"] = station
        station_dict["Name"] = name
        station_dict["Latitude"] = lat
        station_dict["Longitude"] = lon
        station_dict["Elevation"] = el
        stations.append(station_dict)
     
    return jsonify(stations)


#Query the dates and temperature observations of the most active station for the last year of data.
#Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    #calculate the date 1 year  from the most recent date found in the db
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    # List the stations and the counts in descending order. 1st one will be most active
    active_stations = session.query(Measurement.station, func.count()).group_by(Measurement.station).order_by(func.count().desc()).all()

    #select most active station 1st 
    most_active=active_stations[0][0]

    # Query the dates and temperature observations of the most active station for the last year of data.
    temps = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active).filter(Measurement.date >= query_date).all()
    session.close()
    
    tobs_list = []
    #turn results into a dict
    for date, tobs in temps:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        tobs_list.append(tobs_dict)
    
    return jsonify(tobs_list)


#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
#When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
#When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

@app.route("/api/v1.0/<start>")
def date_range_stats(start):
    session = Session(engine)
 
    results= session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
    
    session.close()

    tobs_list = []
    for min,avg,max in results:
        tobs_dict = {}
        tobs_dict["TMin"] = min
        tobs_dict["TAverage"] = avg
        tobs_dict["TMax"] = max
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>/<end>")
def both_date_range_stats(start, end):
    
    session = Session(engine)
    
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    tobs_list = []
    for min,avg,max in results:
        tobs_dict = {}
        tobs_dict["TMin"] = min
        tobs_dict["TAverage"] = avg
        tobs_dict["TMax"] = max
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)


if __name__ == '__main__':
    app.run(debug=True)