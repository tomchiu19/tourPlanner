import sys
import pandas as pd
import numpy as np
import xml.dom.minidom

#from exercise 3
def output_gpx(points, output_filename):
    """
    Output a GPX file with latitude and longitude from the points DataFrame.
    """
    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.8f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.8f' % (pt['lon']))
        trkseg.appendChild(trkpt)

    doc = xml.dom.minidom.getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)

    points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)

    with open(output_filename, 'w') as fh:
        doc.writexml(fh, indent=' ')


def main(input_file):
    culture_tour = pd.read_csv('culture_tour.csv')
    dessert_tour = pd.read_csv('dessert_tour.csv')
    pub_crawl = pd.read_csv('pub_crawl.csv')
    scenic_tour = pd.read_csv('scenic_tour.csv')

    lodging_df = pd.read_csv(input_file)
    lodging_coordinates_df = lodging_df[['lat', 'lon']]
    output_gpx(lodging_coordinates_df, 'lodging.gpx')

    culture_interest = lodging_df['culture'].values[0]
    dessert_interest = lodging_df['dessert'].values[0]
    drinks_interest = lodging_df['drinks'].values[0]
    scenic_interest = lodging_df['scenic'].values[0]

    if (culture_interest == 'y'):
        culture_tour_subset_df = culture_tour[['lat', 'lon']]
        culture_tour_subset_df = culture_tour_subset_df.append(culture_tour_subset_df.iloc[0])
        output_gpx(culture_tour_subset_df, 'culture.gpx')
    if (dessert_interest == 'y'):
        dessert_tour_subset_df = dessert_tour[['lat', 'lon']]
        dessert_tour_subset_df = dessert_tour_subset_df.append(dessert_tour_subset_df.iloc[0])
        output_gpx(dessert_tour_subset_df, 'desserts.gpx')
    if (drinks_interest == 'y'):
        pub_crawl_subset_df = pub_crawl[['lat', 'lon']]
        pub_crawl_subset_df = pub_crawl_subset_df.append(pub_crawl_subset_df.iloc[0])
        output_gpx(pub_crawl_subset_df, 'drinks.gpx')
    if (scenic_interest == 'y'):
        scenic_tour_subset_df = scenic_tour[['lat', 'lon']]
        scenic_tour_subset_df = scenic_tour_subset_df.append(scenic_tour_subset_df.iloc[0])
        output_gpx(scenic_tour_subset_df, 'scenic.gpx')

if __name__ == '__main__':
    input_file = sys.argv[1]
    main(input_file)
