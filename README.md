# Vancouver Area Tour Planner

## Project Idea:

Based on some Vancouver OSM data, I attempted to find various themed tours. These tours include a cultural tour of arts centres, an ice cream tour, a pub crawl, and a scenic bike ride tour. To calculate a tour, try to pass through as many relevant locations as possible within a given time frame, while allowing for some time to stop at each location. Additionally, based on user interests that may exclude certain tours, I calculated an optimal lodging location in order to minimize distances between all tours that the user is interested in.

## Files:

### Code Directory:

**Program pipeline:**

01-extract.py

02-filter.py

03-plan-tours.py

04-find-lodging.py

05-generate-gpx.py

### Data Directory:

**Data:**

amenities-vancouver.json.gz

### Sample Inputs Directory:

**Sample Input:**

sample_user_interests_1.csv

sample_user_interests_2.csv

**Extra Sample Inputs To Generate GPX Files:**

lodging_coordinates_1.csv - for sample_user_interests_1

lodging_coordinates_2.csv - for sample_user_interests_2

## Libraries:

import sys

import pandas as pd

import numpy as np

import math

import random

import xml.dom.minidom

## Instructions:

Running 01-extract.py (produces 'data.csv'):

**python3 01-extract.py data/amenities-vancouver.json.gz data**

Running 02-filter.py (produces 'culture.csv', 'desserts.csv', 'drinks.csv', 'scenic.csv'):

**python3 02-filter.py data.csv**

Running 03-plan-tours.py (produces 'culture_tour.csv', 'dessert_tour.csv', 'pub_crawl.csv', 'scenic_tour.csv'):

**python3 03-plan-tours.py**

Running 04-find-lodging.py (produces 'lodging_coordinates.csv'):

**python3 04-find-lodging.py sample_inputs/sample_user_interests_1.csv**

**or**

**python3 04-find-lodging.py sample_inputs/sample_user_interests_2.csv**

Running 05-generate-gpx.py (produces 'lodging.gpx', possibly 'culture.gpx' / 'desserts.gpx' / 'drinks.gpx' / 'scenic.gpx')

**python3 05-generate-gpx.py lodging_coordinates.csv**
