import os
import json
import pandas
import geopandas
from sqlalchemy import create_engine
from pyproj import CRS
from dotenv import load_dotenv
from pyproj.aoi import AreaOfInterest
from pyproj.database import query_utm_crs_info

load_dotenv()


class SpatialAnalysis:
    """A class contains all utils functions for spatial analysis."""

    def __init__(self, long: str, lat: str) -> None:
        self.long = long
        self.lat = lat
        self.engine = create_engine(
            f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        )

    def convert_to_df(self, file_path: str) -> geopandas.GeoDataFrame:
        """
        Function takes file path(csv, GeoJSON, shapefile(zip)), longitude, and latitude from class\
        constructor function then returns geopandas.GeoDataFrame
        """
        extension = os.path.splitext(file_path)[1]
        if extension == ".csv":
            data_frame = pandas.read_csv(file_path)
            geo_data_frame = geopandas.GeoDataFrame(
                data_frame,
                geometry=geopandas.points_from_xy(
                    data_frame[self.long], data_frame[self.lat]
                ),
            ).dropna(subset=[self.long, self.lat])
            utm_crs_list = query_utm_crs_info(
                datum_name="WGS 84",
                area_of_interest=AreaOfInterest(
                    west_lon_degree=data_frame[self.long].min(),
                    south_lat_degree=data_frame[self.lat].min(),
                    east_lon_degree=data_frame[self.long].max(),
                    north_lat_degree=data_frame[self.lat].max(),
                ),
            )
            utm_crs = CRS.from_epsg(utm_crs_list[0].code)
            if geo_data_frame.crs is None:
                geo_data_frame = geo_data_frame.set_crs(utm_crs)
            geo_data_frame = geo_data_frame.to_crs(utm_crs)
        else:
            geo_data_frame = geopandas.read_file(file_path)
        return geo_data_frame

    def area_of_interest(self, path: list):
        """Receive a list of objects of polygon's points to convert it into a geographic polygon could be intersected for area of interest feature.
        >>> area_of_interest(AreaOfInterestPath)
        return geopandas.GeoDataFrame
        """
        outer_coords = []
        for coord_dict in path:
            inner_coords = []
            inner_coords.append(coord_dict["lng"])
            inner_coords.append(coord_dict["lat"])
            outer_coords.append(inner_coords)
        polygon = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Polygon", "coordinates": [outer_coords]},
                }
            ],
        }
        polygon2json = json.dumps(polygon)
        processed_area = geopandas.read_file(polygon2json)
        return processed_area
