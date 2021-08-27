import sys
import pandas as pd
import numpy as np
import math
import random

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

#attempts to minimize cumulative distance between an optimal midpoint and all tours marked 'interesting'
#couldn't think of a way to loop through only subsets marked as 'interesting', instead this function runs for a max number of iterations and randomly selects points from 'interesting' subsets
def randomized_midpoint_finder(subsets, max_iterations):
    num_subsets = len(subsets)
    for i in range(max_iterations):
        points = []
        shortest_total_distance = sys.maxsize
        for j in range(num_subsets):
            index = random.randint(0, len(subsets[j])-1)
            point = subsets[j][index]
            points.append(point)
            optimal_midpoint = (0, 0)
        test_midpoint = find_midpoint(points)
        total_distance = sum_distances_midpoint(optimal_midpoint, points)
        if(total_distance < shortest_total_distance):
            shortest_total_distance = total_distance
            optimal_midpoint = test_midpoint
    return optimal_midpoint

#finds midpoint of list of points
def find_midpoint(points_array):
    lat = 0
    lon = 0
    num_points = len(points_array)
    for point in points_array:
        lat += point[0]
        lon += point[1]
    lat /= num_points
    lon /= num_points

    return (lat, lon)

#returns total cumulative distance between midpoint and all points considered
def sum_distances_midpoint(midpoint, points_array):
    total_distance = 0
    for point in points_array:
        total_distance += haversine(midpoint, point)
    return total_distance


def main(input_file):
    culture_tour = pd.read_csv('culture_tour.csv')
    dessert_tour = pd.read_csv('dessert_tour.csv')
    pub_crawl = pd.read_csv('pub_crawl.csv')
    scenic_tour = pd.read_csv('scenic_tour.csv')

    user_interests = pd.read_csv(input_file)
    culture_interest = user_interests['culture'].values[0]
    dessert_interest = user_interests['dessert'].values[0]
    drinks_interest = user_interests['drinks'].values[0]
    scenic_interest = user_interests['scenic'].values[0]

    if ((culture_interest == 'n') and (culture_interest == 'n') and (culture_interest == 'n') and (culture_interest == 'n')):
        print("Unable to find lodging")
        return

    culture_tour_subset_df = culture_tour[['lat', 'lon']]
    culture_tour_subset = culture_tour_subset_df.to_records(index=False)
    culture_tour_subset_list = culture_tour_subset.tolist()

    dessert_tour_subset_df = dessert_tour[['lat', 'lon']]
    dessert_tour_subset = dessert_tour_subset_df.to_records(index=False)
    dessert_tour_subset_list = dessert_tour_subset.tolist()

    pub_crawl_subset_df = pub_crawl[['lat', 'lon']]
    pub_crawl_subset = pub_crawl_subset_df.to_records(index=False)
    pub_crawl_subset_list = pub_crawl_subset.tolist()

    scenic_tour_subset_df = scenic_tour[['lat', 'lon']]
    scenic_tour_subset = scenic_tour_subset_df.to_records(index=False)
    scenic_tour_point = [scenic_tour_subset[0]]

    interesting_subsets = []
    if (culture_interest == 'y'):
        interesting_subsets.append(culture_tour_subset_list)
    if (dessert_interest == 'y'):
        interesting_subsets.append(dessert_tour_subset_list)
    if (drinks_interest == 'y'):
        interesting_subsets.append(pub_crawl_subset_list)
    if (scenic_interest == 'y'):
        interesting_subsets.append(scenic_tour_point)

    lodging_coordinates = randomized_midpoint_finder(interesting_subsets, 50000) #run for 50000 iterations, takes ~4s for me (tcc20) when considering all tours, can reduce with not too much variance in coordinates found
    lodging_coordinates_df = user_interests
    lodging_coordinates_df['lat'] = [lodging_coordinates[0]]
    lodging_coordinates_df['lon'] = [lodging_coordinates[1]]
    lodging_coordinates_df.to_csv('lodging_coordinates.csv', index=False)


if __name__ == '__main__':
    input_file = sys.argv[1]
    main(input_file)
