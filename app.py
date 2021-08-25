# import dependencies
from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask import send_file
import os
import pandas as pd
import requests
from windpowerlib import ModelChain, WindTurbine, create_power_curve
from windpowerlib import data as wt
import geopandas
from geopandas.tools import sjoin
import numpy as np
import matplotlib
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
matplotlib.use('Agg')


# Initiate Flask application
app = Flask(__name__)

# Load index.html upon launch
@app.route("/")
def index():
    return render_template("index.html")

# Display results.html
@app.route("/results")
def results():
    return render_template("output.html")

# Download turbineOutput.jpeg
@app.route('/download')
def downloadFile ():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    path = "static/turbineOutput.jpg"
    return send_file(path, as_attachment=True)

# Perform Turbine Analyis
@app.route('/_turbines')
def turbines():
	# Load user inputs from index.html
	latitude = request.args.get('latitude', 0, type=float)
	longitude = request.args.get('longitude', 0, type=float)
	turbType = request.args.get('turb', 0, type=str)
	hubHeight = request.args.get('hubHeight', 0, type=int)

	def get_weather_data(lat, long, filename, **kwargs):
	    """
	    Imports weather data from a file.

	    The data include wind speed at two different heights in m/s, air
	    temperature in two different heights in K, surface roughness length in m
	    and air pressure in Pa. The height in m for which the data applies is
	    specified in the second row.

	    Parameters
	    ----------
	    filename : str
	        Filename of the weather data file.

	    Other Parameters
	    ----------------
	    datapath : str, optional
	        Path where the weather data file is stored.
	        Default is the same directory this is stored in.

	    Returns
	    -------
	    :pandas:`pandas.DataFrame<frame>`
	        DataFrame with time series for wind speed `wind_speed` in m/s,
	        temperature `temperature` in K, roughness length `roughness_length`
	        in m, and pressure `pressure` in Pa.
	        The columns of the DataFrame are a MultiIndex where the first level
	        contains the variable name as string (e.g. 'wind_speed') and the
	        second level contains the height as integer at which it applies
	        (e.g. 10, if it was measured at a height of 10 m). The index is a 
	        DateTimeIndex.

	    """

	    if 'datapath' not in kwargs:
	        kwargs['datapath'] = os.path.dirname(__file__)
	    
	    file = os.path.join(kwargs['datapath'], filename)
	       
	    # read csv file as pandas data frame
	    weather_df = pd.read_csv(
	        file,
	        index_col=0,
	        header=[0, 1],
	        date_parser=lambda idx: pd.to_datetime(idx, utc=True))
	    
		# Creates geopandas data frame for user input point
	    d = pd.DataFrame({'turbine': ["Test"], 'Latitude': [lat], 'Longitude': [long]})
	    point = geopandas.GeoDataFrame(d,geometry=geopandas.points_from_xy(d.Longitude, d.Latitude))
	    point = point.set_crs("EPSG:4326")

	    # Creates geopandas data frame for land cover and surface roughness
	    poly  = geopandas.GeoDataFrame.from_file('madisonLand/landcover.shp')

	    # Performes intersect between user input point and land cover. Saves surface roughness value
	    inp, res = poly.sindex.query_bulk(point.geometry, predicate='intersects')
	    point['intersects'] = np.isin(np.arange(0, len(point)), inp)
	    roughness = poly.loc[res, 'roughness'].values[0]
	  
	  	# Appends surface rouhness to each row of weather date frame
	    rough_col = []
	    for i in range(len(weather_df)):
	        rough_col.append(float(roughness))
	        
	    weather_df.insert(4, ("roughness_length",0), rough_col, True)
	    
	    return weather_df


	def turbine(turbType, hubHeight,weather):

		# Creates wind turbine object from windpowerlib
	    initTurbine = {
	            'turbine_type': turbType,  # turbine type as in oedb turbine library
	            'hub_height': hubHeight  # in m
	        }

	    # initialize WindTurbine object
	    turbine = WindTurbine(**initTurbine)

	    # power output calculation
	    # own specifications for ModelChain setup
	    modelchain_data = {
	        'wind_speed_model': 'logarithmic',      # 'logarithmic' (default),
	                                                # 'hellman' or
	                                                # 'interpolation_extrapolation'
	        'density_model': 'ideal_gas',           # 'barometric' (default), 'ideal_gas'
	                                                #  or 'interpolation_extrapolation'
	        'temperature_model': 'linear_gradient', # 'linear_gradient' (def.) or
	                                                # 'interpolation_extrapolation'
	        'power_output_model':
	            'power_curve',          			# 'power_curve' (default) or
	                                                # 'power_coefficient_curve'
	        'density_correction': True,             # False (default) or True
	        'obstacle_height': 0,                   # default: 0
	        'hellman_exp': None}                    # None (default) or None

	    # initialize ModelChain and use run_model method to calculate power output
	    mcTurbine = ModelChain(turbine, **modelchain_data).run_model(
	        weather)

	    # write power output time series to WindTurbine object
	    turbine.power_output = mcTurbine.power_output

	    return turbine


	def createPlots(turbine, turbType):

	    # plot turbine power output
	    turbine.power_output.plot(legend=True, label= turbType)
	    plt.xlabel('Time')
	    plt.ylabel('Power (Watts)')
	    plt.savefig('static/turbineOutput.jpg', dpi=720)


	def main(lat, long, weatherCSV, turbType, hubHeight):
	    weather = get_weather_data(lat, long, weatherCSV, datapath='')
	    outTurb = turbine(turbType, hubHeight, weather)
	    turbFigure = createPlots(outTurb, turbType)
	    

	main(latitude, longitude, 'MadisonWeather.csv', turbType, hubHeight)
	# opens results page in new web broswer window
	import webbrowser
	webbrowser.open("http://127.0.0.1:5000/results")
	return(render_template("output.html"))


if __name__ == '__main__':
	app.run(debug = True)