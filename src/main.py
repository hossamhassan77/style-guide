import json
from typing import Optional
import uvicorn
from fastapi import FastAPI
from utils import SpatialAnalysis

app = FastAPI()


@app.get("/spatial-analysis/overlay")
async def make_overlay(
    file_path: str,
    long: str,
    lat: str,
    overlay_method: str,
    file_path_two: Optional[str] = None,
    aoi_path: Optional[list] = None,
):
    """
    Perform spatial overlay between GeoDataFrames,\
    Implements several methods that are all effectively subsets of the union.
    operation ('intersection', 'union', 'identity', 'symmetric_difference' or 'difference')
    """
    analysis = SpatialAnalysis(long, lat)
    geo_data_frame = analysis.convert_to_df(file_path)
    if file_path_two:
        second_geo_data_frame = analysis.convert_to_df(file_path)
    else:
        second_geo_data_frame = analysis.area_of_interest(aoi_path)
    overlay_result = geo_data_frame.overlay(
        second_geo_data_frame, how=overlay_method, keep_geom_type=False
    )
    return json.loads(overlay_result.to_json())


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9091)
