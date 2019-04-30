import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station
# Note:  columns for these tables:
# Measurement -- id : int, station : text, date : text, prcp : float, tobs: float
# Station -- id : int, station : text, name : text, latitude : float, longitude : float, elevation : float
# Link Python to DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route('/')
def welcome():
    '''List all available api routes.'''
    return (
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation -- returns final 12 months of precip data as JSON dict<br/>'
        f'/api/v1.0/station -- returns a JSON list of stations<br/>'
        f'/api/v1.0/tobs -- returns JSON list of final 12 months of temperature data <br/>'
        f'/api/v1.0/start -- returns JSON list of temperature data for all dates after start<br/>'
        f'/api/v1.0/start/end -- returns JSON list of temperatures for all dates from start to end<br/>'
        f'Note that start and end are variables to be replaced with dates supplied in YYYY-MM-DD format'
    )


@app.route('/api/v1.0/precipitation')
def dict_precip():
    '''returns final 12 months of precip data as JSON dict'''
    # Calculate final date in data set
    last_date = dt.datetime.strptime(session.query(func.max(Measurement.date)).one()[0], "%Y-%m-%d").date()
    # Calculate the date 1 year ago from the last data point in the database
    final_year_start = last_date.replace(year = last_date.year - 1)
    # Convert the start of the final year to text to use in the query
    final_year_start_text  = final_year_start.strftime("%Y-%m-%d")                                
    # Perform a query to retrieve the data and precipitation scores (filter works on text representation) 
    station_results = session.query(Measurement.station, Measurement.date, Measurement.prcp).\
                    filter(Measurement.date >= final_year_start_text).order_by(Measurement.station).all()
    # Convert the query result to a set of dictionaries, one for each station code
    station_code = ''
    station_dict = dict()
    # station_results rows are tuples having the station code at position 0, date at position 1, precip at position 2
    # rows are ordered by station code
    for row in station_results:
        # When a new station code is encountered, start a new dictionary with it
        if row[0] != station_code:
            station_code = row[0]
            station_dict[station_code] = dict()
        # Write the row info into the inner dictionary
        station_dict[station_code][row[1]] = row[2]

    return jsonify(station_dict)


@app.route('/api/v1.0/station')
def list_stations():
    '''Return a JSON list of stations'''
    # Query the station table
    station_results = session.query(Station.station).distinct().all()
    # Build list
    station_list = [i[0] for i in station_results]  

    return jsonify(station_list)

@app.route('/api/v1.0/tobs')
def dict_tobs():
    '''returns final 12 months of temp data as JSON dict'''
    # Calculate final date in data set
    last_date = dt.datetime.strptime(session.query(func.max(Measurement.date)).one()[0], "%Y-%m-%d").date()
    # Calculate the date 1 year ago from the last data point in the database
    final_year_start = last_date.replace(year = last_date.year - 1)
    # Convert the start of the final year to text to use in the query
    final_year_start_text  = final_year_start.strftime("%Y-%m-%d")                                
    # Perform a query to retrieve the data and precipitation scores (filter works on text representation) 
    station_results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
                    filter(Measurement.date >= final_year_start_text).order_by(Measurement.station).all()
    # Convert the query result to a set of dictionaries, one for each station code
    station_code = ''
    station_dict = dict()
    # station_results rows are tuples having the station code at position 0, date at position 1, tobs at position 2
    # rows are ordered by station code
    for row in station_results:
        # When a new station code is encountered, start a new dictionary with it
        if row[0] != station_code:
            station_code = row[0]
            station_dict[station_code] = dict()
        # Write the row info into the inner dictionary
        station_dict[station_code][row[1]] = row[2]

    return jsonify(station_dict)

@app.route('/api/v1.0/<start>')
def list_key_temp_obs_start(start):
    '''Returns key temperature observations (min, max, average) after given start date'''
    # Return data from query
    obs_results = session.query(Measurement.station,func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
                                        filter(Measurement.date >= start).group_by(Measurement.station)
    # Build results into list, note position 0 = station, 1 = min temp, 2 = max temp, 3 = avg temp
    obs_list = [{'station':row[0], 'min':row[1], 'max':row[2], 'avg':row[3]} for row in obs_results]

    return jsonify(obs_list)

@app.route('/api/v1.0/<start>/<end>')
def list_key_temp_obs_start_end(start, end):
    '''Return key temperature observations (min, max, and average) for given start, end date range'''
    # Reutrn data from query
    obs_results = session.query(Measurement.station,func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
                                       filter(and_(Measurement.date >= start, Measurement.date <= end)).\
                                       group_by(Measurement.station)
    # Build results into list, note position 0 = station, 1 = min temp, 2 = max temp, 3 = avg temp
    obs_list = [{'station':row[0], 'min':row[1], 'max':row[2], 'avg':row[3]} for row in obs_results]

    return jsonify(obs_list)

if __name__ == '__main__':
    app.run(debug=True, threaded=False)
