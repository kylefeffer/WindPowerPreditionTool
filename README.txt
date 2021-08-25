# Wind Power Projection Tool

This is a project created by Kyle Feffer for his final practicum in GEOG778 at the University of Wisconsin-Maidson.

## Dependencies

Flask 2.0.1 - https://pypi.org/project/Flask/
geopandas 0.9.0 - https://geopandas.org/
matplotlib 3.4.3 - https://matplotlib.org/
numpy 1.21.2 - https://numpy.org/
pandas 1.3.2 - https://pandas.pydata.org/
windpowerlib 0.2.1 - https://github.com/wind-python/windpowerlib 

## Usage

```python
# runs application
app.py
```

## Project Purpose

One of the largest roadblocks in the transition to a more sustainable form of energy generation is the planning and construction of new renewable energy generation facilities. As land developers and engineers plan the layout of new wind projects, there are several variables that impact the final design. These include landowner participation, mandatory setbacks, hazard areas, local topography, and perhaps most importantly, potential wind power generation. This application aims to provide engineers and land developers an easy-to-use tool to help assess potential wind power generation on their projects to help work through the most challenging variable to calculate.

To evaluate this information, several key pieces of information are needed. First and perhaps most obviously, the application must take in and evaluate local environmental data. For this application, environmental data was obtained though the National Centers for Environmental Information (https://www.ncdc.noaa.gov/cdo-web/) run by the National Oceanic and Atmospheric Administration (NOAA). From here, a series of surface level environmental data sets were obtained, and data aloft was interpolated as descried in the Model Methodology section of this paper.

The next key variable needed to perform this analysis is the surface roughness length over the terrain. While there are several methodologies for evaluating surface roughness length, this application took data from the Multi-Resolution Land Characteristics Consortium (https://www.mrlc.gov/data) hosted by the United States Geological Survey (USGS). This data set categorizes the land cover values into a series of discrete classifications which were then cross referenced with information from E. Linacre and B. Geerts (1999) (http://www-das.uwyo.edu/~geerts/cwx/notes/chap14/roughness.html) to obtain surface roughness length values.

Lastly, each type of wind turbine has a specific power curve that allows it to generate energy at a different rate based on the wind patterns impacting it. To acquire these wind curve values, an open-source python module called windpowerlib (https://github.com/wind-python/windpowerlib) was installed and used in the analysis process. By putting all these variables together, this application can help model the projected power generation of a specific model of wind turbine at a given location. 

## Contributing

Pull requests are welcome. Please contact the developer to discuss any chages to the source code.