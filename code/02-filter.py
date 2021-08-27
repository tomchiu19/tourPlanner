import sys
import pandas as pd
import numpy as np


#one attempt to find "interesting" places
def place_of_interest(row):
    if ('brand' in row):
        return False
    if ('information' in row):
        return False
    if ('wikidata' in row):
        return True
    if ('tourism' in row):
        return True
    return False

def find_place_of_interest(dataframe):
    dataframe['interesting'] = dataframe['tags'].apply(place_of_interest)

    dataframe = dataframe[dataframe['interesting'] == True]

    return dataframe

def amenity_subset(dataframe, subset):
    frames = []
    for amenity in subset:
        frame = []
        frame = dataframe[dataframe['amenity'] == amenity]
        frames.append(frame)
    return pd.concat(frames)


def main(input_file):
    cultural_amenities = ['arts_centre']
    #meal_amenities = ['restaurant'] #didn't end up using
    dessert_amenities = ['ice_cream']
    drink_amenities = ['pub']
    scenic_amenities = ['bicycle_rental', 'fountain']
    unfiltered_scenic_amenities = ['bench', 'clock', 'theatre']
    #activity_amenities = ['boat_rental', 'casino', 'nightclub', 'spa'] #didn't end up using

    osm_data = pd.read_csv(sys.argv[1])

    osm_data = osm_data[osm_data['name'].notnull()]
    osm_data = osm_data[['lat', 'lon', 'amenity', 'name', 'tags']]
    osm_data = osm_data.sort_values(by=['amenity'])

    culture = amenity_subset(osm_data, cultural_amenities)
    #meals = amenity_subset(osm_data, meal_amenities)
    desserts = amenity_subset(osm_data, dessert_amenities)
    drinks = amenity_subset(osm_data, drink_amenities)

    scenic = amenity_subset(osm_data, scenic_amenities)
    unfiltered_scenic = find_place_of_interest(amenity_subset(osm_data, unfiltered_scenic_amenities))
    scenic = pd.concat([scenic, unfiltered_scenic])

    #activities = amenity_subset(osm_data, activity_amenities)

    culture.to_csv('culture.csv', index=False)
    #meals.to_csv('meals.csv', index=False)
    desserts.to_csv('desserts.csv', index=False)
    drinks.to_csv('drinks.csv', index=False)
    scenic.to_csv('scenic.csv', index=False)
    #activities.to_csv('activities.csv', index=False)


if __name__ == '__main__':
    input_file = sys.argv[1]
    main(input_file)
