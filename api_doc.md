**Spatial Analysis — Overlay Endpoint**

- **Path:** `GET /spatial-analysis/overlay`
- **Description:** Perform a spatial overlay between two vector datasets (GeoDataFrames). Supports methods such as `intersection`, `union`, `identity`, `symmetric_difference`, and `difference`.

**Query Parameters**
- **`file_path`**: string — *required*; path or URL to the primary vector file (e.g., GeoJSON, Shapefile).
- **`long`**: string — *required*; name of the longitude (or X) field/column in the input data.
- **`lat`**: string — *required*; name of the latitude (or Y) field/column in the input data.
- **`overlay_method`**: string — *required*; one of `intersection`, `union`, `identity`, `symmetric_difference`, `difference`.
- **`file_path_two`**: string — *optional*; path or URL to the second vector file to overlay with. If omitted, the endpoint will attempt to use `aoi_path`.
- **`aoi_path`**: array of strings — *optional*; one or more AOI (area-of-interest) paths. Can be passed by repeating the query parameter (e.g. `?aoi_path=/p/a.geojson&aoi_path=/p/b.geojson`) or as a JSON array depending on client tooling.

**Response**
- **Content-Type:** `application/json`
- **Body:** GeoJSON-like object produced from the overlay result. Typically a `FeatureCollection` with `features` containing geometries and properties.

**Example Request (PowerShell)**
```powershell
Invoke-RestMethod -Method Get -Uri "http://localhost:9091/spatial-analysis/overlay?file_path=C:\data\layer1.geojson&long=lon&lat=lat&overlay_method=intersection&aoi_path=C:\data\aoi.geojson"
```

**Example Request (curl)**
```bash
curl "http://localhost:9091/spatial-analysis/overlay?file_path=/data/layer1.geojson&long=lon&lat=lat&overlay_method=intersection&aoi_path=/data/aoi.geojson"
```

**Example Response (trimmed)**
```json
{
	"type": "FeatureCollection",
	"features": [
		{
			"type": "Feature",
			"properties": {"id": 1, "some_prop": "value"},
			"geometry": {"type": "Polygon", "coordinates": [[[...]]]} 
		}
	]
}
```

**Notes & Implementation Details**
- **Behavior when `file_path_two` omitted:** If `file_path_two` is not provided, the endpoint uses `aoi_path` to construct the second GeoDataFrame.
- **Implementation note:** Current code in `src/main.py` contains a probable bug: when `file_path_two` is provided the implementation calls `analysis.convert_to_df(file_path)` again (re-using the first path) instead of `file_path_two`. This causes the overlay to run between the same dataset twice. Consider changing the line to use `file_path_two`.
- **Errors:** The endpoint will raise HTTP 422 if required query parameters are missing. Errors raised by the `SpatialAnalysis` helper or file parsing will be returned as 5xx unless explicitly handled.

**Suggested Next Steps**
- Add parameter validation and clearer error responses (e.g., 400 for invalid files).
- Fix the `file_path_two` bug in `src/main.py` to use the provided second path.
- Add example curl/PowerShell commands that use accessible sample data in the repo.

**Files**
- Implementation: `src/main.py`

