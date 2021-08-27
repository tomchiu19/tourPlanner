import sys
import pandas as pd
import numpy as np
import math

#average walking speed = 3-4 miles/hour = 80-110 meters/minute - will use 100 meters/minute
walking_speed = 100
#average biking speed = 10-14 miles/hour = 270-375 meters/minute - will use 300 meters/minute
biking_speed = 300

#adapted from: https://stackoverflow.com/questions/25767596/vectorised-haversine-formula-with-a-pandas-dataframe
def  haversine(point1, point2):
    lat1 = point1[0]
    lon1 = point1[1]
    lat2 = point2[0]
    lon2 = point2[1]
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    m = 6367000 * c
    return m

def walking_time_elapsed(point1, point2):
    return (haversine(point1, point2) / walking_speed)

def biking_time_elapsed(point1, point2):
    return (haversine(point1, point2) / biking_speed)

#returns index of next closest unvisited point and distance to that point
#current is a tuple - (lat, lon)
#unvisited is a numpy recarray of coordinate tuples - [(lat, lon) (lat, lon) ... (lat, lon)]
def greedy_find_next_point(current, unvisited):
    min_distance = sys.maxsize
    index_closest = 0
    for i in range(len(unvisited)):
            next_point = unvisited[i]
            point_distance = haversine(current, next_point)
            if (point_distance < min_distance):
                index_closest = i
                min_distance = point_distance
    return [index_closest, min_distance]

#returns list of tuples indicating the maximum length route possible from subset points
#points is a numpy recarray of coordinate tuples - [(lat, lon) (lat, lon) ... (lat, lon)]
#time_limit is the time limit of the route in minutes
#stopping_time is the time allotted to stop at each location in minutes
#unrealistic as it takes birds eye distance, not sure how to incorporate street or even traffic information
def greedy_route_planner(points, time_limit, stopping_time, means_of_transportation):
    if (means_of_transportation == 'walking'):
        speed = walking_speed
    elif (means_of_transportation == 'biking'):
        speed = biking_speed
    route = []
    max_route_size = 0
    max_route_time_remaining = 0
    for i in range(len(points)):
        time_available = time_limit - stopping_time #stop at first location
        return_trip_time = 0
        starting_point = points[i]
        curr = starting_point
        test_route = []
        test_route_size = 0
        test_route.append(starting_point)
        unvisited_points = np.delete(points, i, axis=0)
        while (return_trip_time < time_available):
            [next_index, next_distance] = greedy_find_next_point(curr, unvisited_points)
            time_elapsed = next_distance / walking_speed
            time_elapsed += stopping_time
            if (means_of_transportation == 'walking'):
                return_trip_time = walking_time_elapsed(starting_point, unvisited_points[next_index])
            elif (means_of_transportation == 'biking'):
                return_trip_time = biking_time_elapsed(starting_point, unvisited_points[next_index])
            time_available -= time_elapsed
            if (return_trip_time < time_available):
                test_route_size += 1
                curr = unvisited_points[next_index]
                test_route.append(curr)
                unvisited_points = np.delete(unvisited_points, next_index, axis=0)
            else:
                test_route.append(starting_point)
        if (test_route_size > max_route_size):
            max_route_size = test_route_size
            max_route_time_remaining = time_available
            route = test_route
        elif ((test_route_size == max_route_size) and (time_available > max_route_time_remaining)): #tiebreaker, take the shorter path
            max_route_time_remaining = time_available
            route = test_route

    return route

#returns list of tuples indicating the maximum length route possible from subset points, when starting from a separate subset
#starting_points is a numpy recarray of coordinate tuples - [(lat, lon) (lat, lon) ... (lat, lon)]
#locations is a numpy recarray of coordinate tuples - [(lat, lon) (lat, lon) ... (lat, lon)]
#time_limit is the time limit of the route in minutes
#stopping_time is the time allotted to stop at each location in minutes
#unrealistic as it takes birds eye distance, not sure how to incorporate street or even traffic information
def start_specific_greedy_route_planner(starting_points, locations, time_limit, stopping_time, means_of_transportation):
    if (means_of_transportation == 'walking'):
        speed = walking_speed
    elif (means_of_transportation == 'biking'):
        speed = biking_speed
    route = []
    max_route_size = 0
    max_route_time_remaining = 0
    for i in range(len(starting_points)):
        time_available = time_limit - stopping_time #stop at first location
        return_trip_time = 0
        starting_point = starting_points[i]
        curr = starting_point
        test_route = []
        test_route_size = 0
        test_route.append(starting_point)
        unvisited_points = locations
        while (return_trip_time < time_available):
            [next_index, next_distance] = greedy_find_next_point(curr, unvisited_points)
            time_elapsed = next_distance / speed
            time_elapsed += stopping_time
            if (means_of_transportation == 'walking'):
                return_trip_time = walking_time_elapsed(starting_point, unvisited_points[next_index])
            elif (means_of_transportation == 'biking'):
                return_trip_time = biking_time_elapsed(starting_point, unvisited_points[next_index])
            time_available -= time_elapsed
            if (return_trip_time < time_available):
                test_route_size += 1
                curr = unvisited_points[next_index]
                test_route.append(curr)
                unvisited_points = np.delete(unvisited_points, next_index, axis=0)
            else:
                test_route.append(starting_point)
        if (test_route_size > max_route_size):
            max_route_size = test_route_size
            max_route_time_remaining = time_available
            route = test_route
        elif ((test_route_size == max_route_size) and (time_available > max_route_time_remaining)): #tiebreaker, take the shorter path
            max_route_time_remaining = time_available
            route = test_route

    return route

#test function for roundtrip time of route planned
def test_time_of_route(route, means_of_transportation, stopping_time):
    locations_visited = len(route) - 1
    total_time = locations_visited * stopping_time
    if (means_of_transportation == 'walking'):
        for i in range(locations_visited):
            total_time += walking_time_elapsed(route[i], route[i+1])
    elif (means_of_transportation == 'biking'):
        for i in range(locations_visited):
            total_time += biking_time_elapsed(route[i], route[i+1])
    return total_time

#returns list of names of locations visited during tour
def find_locations_from_route(route, dataframe):
    locations_visited = len(route) - 1
    locations = []
    for i in range(locations_visited):
        point = route[i]
        point_lat = point[0]
        point_lon = point[1]
        location = dataframe[dataframe['lat'] == point_lat]
        location = location[location['lon'] == point_lon]
        location_name = location['name'].values[0]
        locations.append(location_name)
    return locations

#returns list of distances in km to the next location in the tour
def find_distances_from_route(route):
    distances = []
    for i in range(len(route) - 1):
        distance = round((haversine(route[i], route[i+1]) / 1000), 2)
        distances.append(distance)
    return distances

#returns list of lat coordinates of all locations visited in the tour
def find_lat_from_route(route):
    lat_coordinates = []
    for i in range(len(route) - 1):
        coordinate = route[i][0]
        lat_coordinates.append(coordinate)
    return lat_coordinates

#returns list of lon coordinates of all locations visited in the tour
def find_lon_from_route(route):
    lon_coordinates = []
    for i in range(len(route) - 1):
        coordinate = route[i][1]
        lon_coordinates.append(coordinate)
    return lon_coordinates


def main():
    culture = pd.read_csv('culture.csv')
    #meals = pd.read_csv('meals.csv') #didn't end up using
    desserts = pd.read_csv('desserts.csv')
    drinks = pd.read_csv('drinks.csv')
    scenic = pd.read_csv('scenic.csv')
    #activities = pd.read_csv('activities.csv') #didn't end up using


    #cultural tour - walk around the city - plan for 8 hour tour, stop at each location for 30 minutes, visit as many as possible
    #cultural tour subset is only 11 locations, don't need to split it up when planning tour

    culture_points_df = culture[['lat', 'lon']]
    culture_points = culture_points_df.to_records(index=False)
    culture_route = greedy_route_planner(culture_points, 480, 30, 'walking') #max trip time = 480 minutes, stop at each location for 30 minutes
    culture_tour_locations = find_locations_from_route(culture_route, culture)
    culture_tour_distances = find_distances_from_route(culture_route)
    culture_tour_lat_coordinates = find_lat_from_route(culture_route)
    culture_tour_lon_coordinates = find_lon_from_route(culture_route)
    culture_tour_df = pd.DataFrame(data = {'location': culture_tour_locations, 'distance to next location (km)': culture_tour_distances, 'lat': culture_tour_lat_coordinates, 'lon': culture_tour_lon_coordinates})
    culture_tour_df.to_csv('culture_tour.csv', index=False)


    #dessert tour - walk around the city - plan for 4 hour tour, stop at each location for 30 minutes, visit as many places as possible
    #icecream tour subset is 71 locations, was planning on clustering and running on subsets but it runs fast anyways

    dessert_points_df = desserts[['lat', 'lon']]
    dessert_points = dessert_points_df.to_records(index=False)
    dessert_route = greedy_route_planner(dessert_points, 240, 30, 'walking') #max trip time = 240 minutes, stop at each location for 30 minutes
    dessert_tour_locations = find_locations_from_route(dessert_route, desserts)
    dessert_tour_distances = find_distances_from_route(dessert_route)
    dessert_tour_lat_coordinates = find_lat_from_route(dessert_route)
    dessert_tour_lon_coordinates = find_lon_from_route(dessert_route)
    dessert_tour_df = pd.DataFrame(data = {'location': dessert_tour_locations, 'distance to next location (km)': dessert_tour_distances, 'lat': dessert_tour_lat_coordinates, 'lon': dessert_tour_lon_coordinates})
    dessert_tour_df.to_csv('dessert_tour.csv', index=False)


    #pub crawl - walk around the city - plan for 3 hours, stop at each location for 20 minutes, visit as many places as possible
    #pub crawl subset is 186 locations, still runs in a reasonable timeframe without clustering

    pub_points_df = drinks[['lat', 'lon']]
    pub_points = pub_points_df.to_records(index=False)
    pub_route = greedy_route_planner(pub_points, 180, 20, 'walking') #max trip time = 180 minutes, stop at each location for 20 minutes
    pub_crawl_locations = find_locations_from_route(pub_route, drinks)
    pub_crawl_distances = find_distances_from_route(pub_route)
    pub_crawl_lat_coordinates = find_lat_from_route(pub_route)
    pub_crawl_lon_coordinates = find_lon_from_route(pub_route)
    pub_crawl_df = pd.DataFrame(data = {'location': pub_crawl_locations, 'distance to next location (km)': pub_crawl_distances, 'lat': pub_crawl_lat_coordinates, 'lon': pub_crawl_lon_coordinates})
    pub_crawl_df.to_csv('pub_crawl.csv', index=False)


    #scenic bike ride - plan for 8 hour bike ride, start at bicycle_rental, stop at each location for 2 minutes, visit as many other locations as possible
    #scenic tour starting point subset is 201 locations, location subset is 26 locations, runs in reasonable time without clustering

    scenic_start_points_df = scenic[scenic['amenity'] == 'bicycle_rental']
    scenic_start_points_df = scenic_start_points_df[['lat', 'lon']]
    scenic_location_points_df = scenic[scenic['amenity'] != 'bicycle_rental']
    scenic_location_points_df = scenic_location_points_df[['lat', 'lon']]
    scenic_start_points = scenic_start_points_df.to_records(index=False)
    scenic_location_points = scenic_location_points_df.to_records(index=False)
    scenic_route = start_specific_greedy_route_planner(scenic_start_points, scenic_location_points, 480, 2, 'biking') #max trip time = 480 minutes, stop at each location for 2 minutes
    scenic_tour_locations = find_locations_from_route(scenic_route, scenic)
    scenic_tour_distances = find_distances_from_route(scenic_route)
    scenic_tour_lat_coordinates = find_lat_from_route(scenic_route)
    scenic_tour_lon_coordinates = find_lon_from_route(scenic_route)
    scenic_tour_df = pd.DataFrame(data = {'location': scenic_tour_locations, 'distance to next location (km)': scenic_tour_distances, 'lat': scenic_tour_lat_coordinates, 'lon': scenic_tour_lon_coordinates})
    scenic_tour_df.to_csv('scenic_tour.csv', index=False)


if __name__ == '__main__':
    main()
