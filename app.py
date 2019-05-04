import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database Setup
engine = create_engine('sqlite:///Resources/hawaii.sqlite')


Base = automap_base()

Base.prepare(engine, reflect=True)


Measurement = Base.classes.measurement
Station = Base.classes.station


session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
        f"NOTE: start_date and end_date must be of the form YYYYMMDD"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    results = session.query(Measurement.date, Measurement.prcp).all()

    precip_rslts = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict[date] = prcp
        precip_rslts.append(precip_dict)

    return jsonify(precip_rslts)

@app.route("/api/v1.0/stations")
def stations():
    
    results = session.query(Station.station).all()
    all_stations = [s[0] for s in results]

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    
    latest_date = session.query(Measurement.date).\
        order_by(Measurement.date.desc()).first()
    l_date = dt.datetime.strptime(latest_date[0], '%Y-%m-%d')
    p_yr = l_date - dt.timedelta(days=365)
    
    results = session.query(Measurement.tobs).\
        filter(Measurement.date >= p_yr).all()
    last_yr_temps = [r[0] for r in results]
    
    return jsonify(last_yr_temps)

@app.route("/api/v1.0/<start>")
def start_date(start):

    start_date = f'{start}'
    start_date = f'{start_date[0:4]}-{start_date[4:6]}-{start_date[6:8]}'
    s_date = dt.datetime.strptime(start_date, '%Y-%m-%d')
    
    # latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    # latest_date = dt.datetime.strptime(latest_date[0], '%Y-%m-%d')

    # early_date = session.query(Measurement.date).order_by(Measurement.date.asc()).first()
    # early_date = dt.datetime.strptime(early_date[0], '%Y-%m-%d')

    sel = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    
    results = session.query(*sel).\
        filter(Measurement.date >= s_date).all()
    
    tmin = results[0][0]
    tmax = results[0][1]
    tavg = results[0][2]

    return (
        f'TMIN: {tmin} <br/>'
        f'TAVG: {tavg} <br/>'
        f'TMAX: {tmax} <br/>'
    )


@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    

    start_date = f'{start}'
    start_date = f'{start_date[0:4]}-{start_date[4:6]}-{start_date[6:8]}'
    s_date = dt.datetime.strptime(start_date, '%Y-%m-%d')

    end_date = f'{end}'
    end_date = f'{end_date[0:4]}-{end_date[4:6]}-{end_date[6:8]}'
    e_date = dt.datetime.strptime(end_date, '%Y-%m-%d')

    # latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    # latest_date = dt.datetime.strptime(latest_date[0], '%Y-%m-%d')

    # early_date = session.query(Measurement.date).order_by(Measurement.date.asc()).first()
    # early_date = dt.datetime.strptime(early_date[0], '%Y-%m-%d')
    
    sel = [func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    
    results = session.query(*sel).\
        filter(Measurement.date >= s_date).\
        filter(Measurement.date <= e_date).all()
    
    tmin = results[0][0]
    tmax = results[0][1]
    tavg = results[0][2]
    
    print(type(start))

    return (
        f'TMIN: {tmin} <br/>'
        f'TAVG: {tavg} <br/>'
        f'TMAX: {tmax} <br/>'
        
    )
    

if __name__ == "__main__":
    app.run(debug=False)