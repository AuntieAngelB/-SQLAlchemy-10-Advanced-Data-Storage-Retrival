import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import sqlite3
# Database Setup
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)


@app.route("/")
def home():
    return(
"<h1> List of all available api routes: </h1>\
    <ul>\
            <li> <strong> /api/v1.0/precipitation: </strong> Convert query results to a dictionary using date as the key and prcp as the value; returns a JSON </li>\
            <li> <strong> /api/v1.0/stations: </strong> Returns a JSON list of stations from the dataset </li>\
            <li> <strong> /api/v1.0/tobs: </strong> Query the dates and temperature observations from a year from the last data point </li>\
            <li> <strong> /api/v1.0/start: </strong> Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date </li>\
            <li> <strong> /api/v1.0/start/end: </strong> Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start and end date </li>\
    </ul>"
          )

@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date.asc()).all()
    return jsonify(results)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station, Station.name).all()
    return jsonify(results)

@app.route("/api/v1.0/tobs")
def temps():
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-18').all()
    return jsonify(results)

@app.route('/api/v1.0/<start>')
def temp_start_stats(start):
    results = session.query\
        (func.min(Measurement.tobs).label('min'),\
        func.avg(Measurement.tobs).label('average'),\
        func.max(Measurement.tobs).label('max'))\
        .filter(Measurement.date >= start).all()

    start_stats_data = []
    for row in results:
        start_stats_dict = {}
        start_stats_dict['Start Date'] = start
        start_stats_dict['Min Temp'] = row.min
        start_stats_dict['Avg Temp'] = row.average
        start_stats_dict['Max Temp'] = row.max
        start_stats_data.append(start_stats_dict)
        
    return jsonify(start_stats_dict)
    
@app.route("/api/v1.0/<start>/<end>")
def temp_stats_start_end(start, end):

    results = session.query(func.min(Measurement.tobs).label('min'),\
    func.avg(Measurement.tobs).label('avg'),\
    func.max(Measurement.tobs).label('max'))\
    .filter(Measurement.date >= start)\
    .filter(Measurement.date <= end).all()

    start_end_stats_data = []
    for row in results:
        start_end_stats_dict = {}
        start_end_stats_dict['Start Date'] = start
        start_end_stats_dict['End Date'] = end
        start_end_stats_dict['Min Temp'] = row.min
        start_end_stats_dict['Avg Temp'] = row.avg
        start_end_stats_dict['Max Temp'] = row.max
        start_end_stats_data.append(start_end_stats_dict)
    
    return jsonify(start_end_stats_data)

if __name__ == '__main__':
    app.run(debug=True)

