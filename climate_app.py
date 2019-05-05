import numpy as np
import pandas as pd
import datetime as dt
from flask import Flask, jsonify

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################
# Setting everything up: 
#################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#################################
# Flask setup: 
#################################
app = Flask(__name__)

#################################
# Flask Routes: 
#################################
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Welcome to the home page.<br/>"
        f"Here is a list of all the available routes: <br/>"
        f"Total precipitation recorded from the previous year: /api/v1.0/precipitation <br/>"
        f"List of stations: /api/v1.0/stations <br/>"
        f"List of last year temperatures recorded from each station: /api/v1.0/tobs <br/>"
        f"Calcuates the min/avg/max temperature for all dates equal to or greater than start date: /api/v1.0/start<br/>"
        f"Calculates the min/avg/max temperature for all dates between end and start dates: /api/v1.0/start_end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """List total precipitation from previous recorded year"""

    session = Session(engine)
    last_year = '2016-08-23'
    rain = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>=last_year).order_by(Measurement.date).all()
    return(jsonify(rain))

@app.route("/api/v1.0/stations")
def stations():
    """Lists of stations"""
    session = Session(engine)
    active_stations = (session.query(Measurement.station, func.count(Measurement.station))
                        .order_by(func.count(Measurement.station).desc()).group_by(Measurement.station).all())
    return(jsonify(active_stations))

active_stations = (session.query(Measurement.station, func.count(Measurement.station))
                    .order_by(func.count(Measurement.station).desc()).group_by(Measurement.station).all())

@app.route("/api/v1.0/tobs")
def tobs():
    """Lists of last year temperatures recorded from each station"""
    session = Session(engine)
    # most_active = active_stations[0][0]
    last_year = '2016-08-23'
    highest_obs = (session.query(Measurement.station, Measurement.tobs)
                    .filter(Measurement.station == "USC00519281").filter(Measurement.date >= last_year).all())
    return(jsonify(highest_obs))

@app.route("/api/v1.0/<start>")
def start(start=None):
    """Calcuates the min/avg/max temperature for all dates equal to or greater than start date"""
    session = Session(engine)
    start = (session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))
            .filter(Measurement.date >= "2016-08-23").all())
    return(jsonify(start))

@app.route("/api/v1.0/<start>/<end>")
def start_end(start=None, end=None):
    """Calculates the min/avg/max temperature for all dates between end and start dates"""
    session = Session(engine)
    start_end = (session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))
                .filter(Measurement.date >= "2016-08-23").filter(Measurement.date <= "2017-08-23").all())
    return(jsonify(start_end))


if __name__ == "__main__":
    app.run(debug=True) 