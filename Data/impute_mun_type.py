import numpy as np
import pandas as pd
import geopandas as gpd
import shapely.geometry as geo
from sklearn.neighbors import KDTree
import random

REFERENCE_YEAR = 2018

SHAPEFILES = [
    (2018, "municipality_borders/gd-b-00.03-875-gg18/ggg_2018-LV95/shp/g1g18.shp", "GMDNR", "GMDNAME"),
    (2017, "municipality_borders/gd-b-00.03-875-gg17/ggg_2017/shp/LV95/g1g17.shp", "GMDNR", "GMDNAME"),
    (2016, "municipality_borders/gd-b-00.03-875-gg16/ggg_2016/shp/g1g16.shp", "GMDNR", "GMDNAME"),
    (2015, "municipality_borders/gd-b-00.03-876-gg15/GGG_15_V161025/shp/g1g15.shp", "GMDNR", "GMDNAME"),
    (2014, "municipality_borders/gd-b-00.03-877-gg14/ggg_2014/shp/g1g14.shp", "GMDNR", "GMDNAME"),
    (2013, "municipality_borders/gd-b-00.03-877-gg13_r1/ggg_2013/shp/g1g13.shp", "GMDNR", "GMDNAME"),
    (2012, "municipality_borders/gd-b-00.03-878-gg12/g1g12_shp_121130/G1G12.shp", "GMDE", "NAME"),
    (2011, "municipality_borders/gd-b-00.03-879-gg11/g1g11_shp_121130/G1G11.shp", "GMDE", "NAME"),
    (2010, "municipality_borders/gd-b-00.03-880-gg10/g1g10_shp_121130/G1G10.shp", "GMDE", "NAME"),
    (2009, "municipality_borders/gd-b-00.03-881-gg09g1/g1g09_shp_090626/G1G09.shp", "GMDE", "NAME")
]

def create_df_municipalities():
    data_path = "/nas/ivtmatsim/scenarios/switzerland/data/"
    
    df_all = []
    all_ids = set()

    # Load all the shape files, only add the municipalities that haven't been found before
    for year, shapefile, id_field, name_field in SHAPEFILES:
        df = gpd.read_file(
            "%s/%s" % (data_path, shapefile),
            encoding="latin1"
        ).to_crs("epsg:2056")

        df.crs = "epsg:2056"

        df.loc[:, "municipality_id"] = df[id_field]
        df.loc[:, "municipality_name"] = df[name_field]
        df.loc[:, "year"] = year

        df_ids = set(np.unique(df["municipality_id"]))
        df_new_ids = df_ids - all_ids

        df_all.append(
            df[df["municipality_id"].isin(df_new_ids)][["municipality_id", "municipality_name", "year", "geometry"]])
        all_ids |= df_new_ids

    df_all = pd.concat(df_all)

    df_reference = gpd.GeoDataFrame(df_all[df_all["year"] == REFERENCE_YEAR])
    df_reference.crs = df_all.crs

    df_deprecated = gpd.GeoDataFrame(df_all[df_all["year"] != REFERENCE_YEAR])
    df_deprecated["deprecated_municipality_id"] = df_deprecated["municipality_id"]
    del df_deprecated["municipality_id"]
    df_deprecated["geometry"] = df_deprecated.centroid
    df_deprecated.crs = df_all.crs

    # For each deprecated municipality find the covering reference municipality
    df_mapping = gpd.sjoin(
        df_reference, df_deprecated, op="contains"
    ).reset_index()[["municipality_id", "deprecated_municipality_id"]]

    # Now we are left over with some old municipalities whose centroids
    # are not covered by any new municipality (mainly at the border and
    # close to lakes). Therefore, we do another run and find the current
    # municipality with the closes distance (more expensive operation).

    missing_ids = set(
        np.unique(df_deprecated["deprecated_municipality_id"])
    ) - set(np.unique(df_mapping["deprecated_municipality_id"]))

    df_missing = df_deprecated[
        df_deprecated["deprecated_municipality_id"].isin(missing_ids)
    ][["deprecated_municipality_id", "geometry"]]

    coordinates = np.vstack([df_reference["geometry"].centroid.x, df_reference["geometry"].centroid.y]).T
    kd_tree = KDTree(coordinates)

    coordinates = np.vstack([df_missing["geometry"].x, df_missing["geometry"].y]).T
    indices = kd_tree.query(coordinates, return_distance=False).flatten()

    df_missing.loc[:, "municipality_id"] = df_reference.iloc[indices]["municipality_id"].values
    df_missing = df_missing[["municipality_id", "deprecated_municipality_id"]]

    df_existing = pd.DataFrame(df_reference[["municipality_id"]])
    df_existing["deprecated_municipality_id"] = df_existing["municipality_id"]

    df_mapping = pd.concat([df_existing, df_mapping, df_missing])
    df_reference = df_reference[["municipality_id", "municipality_name", "geometry"]]

    return df_reference, df_mapping

def update_municipality_ids(df, df_mapping, remove_unknown=False):
    assert ("municipality_id" in df.columns)

    df["deprecated_municipality_id"] = df["municipality_id"]
    del df["municipality_id"]

    df_join = pd.merge(
        df[["deprecated_municipality_id"]], df_mapping,
        on="deprecated_municipality_id", how="left"
    )

    df.loc[:, "municipality_id"] = df_join.loc[:, "municipality_id"].values

    if remove_unknown:
        return df[~np.isnan(df["municipality_id"])]
    else:
        return df


def municipality_types(df_municipalities):
    # Load data
    data_path = "/nas/ivtmatsim/scenarios/switzerland/data"

    df_types = pd.read_excel("%s/spatial_structure_2018.xlsx" % data_path,
                             names=["municipality_id", "TYP"],
                             usecols=[0, 21],
                             skiprows=6,
                             nrows=2229,
                             )

    # Rewrite classification
    df_types.loc[df_types["TYP"] == 1, "municipality_type"] = "urban"
    df_types.loc[df_types["TYP"] == 2, "municipality_type"] = "urban"
    df_types.loc[df_types["TYP"] == 3, "municipality_type"] = "suburban"
    df_types.loc[df_types["TYP"] == 4, "municipality_type"] = "urban"
    df_types.loc[df_types["TYP"] == 5, "municipality_type"] = "suburban"
    df_types.loc[df_types["TYP"] == 6, "municipality_type"] = "rural"
    df_types.loc[df_types["TYP"] == 7, "municipality_type"] = "rural"
    df_types.loc[df_types["TYP"] == 8, "municipality_type"] = "rural"
    df_types.loc[df_types["TYP"] == 9, "municipality_type"] = "rural"

    df_types["municipality_type"] = df_types["municipality_type"].astype("category")
    df_types = df_types[["municipality_id", "municipality_type"]]

    # Match by municipality_id
    df_existing = pd.merge(df_municipalities, df_types, on="municipality_id")
    df_existing["imputed_municipality_type"] = False
    df_existing = df_existing[["municipality_id", "municipality_type", "imputed_municipality_type", "geometry"]]

    # Some ids are missing (because they are special zones)
    df_missing = gpd.GeoDataFrame(df_municipalities[
                                      ~df_municipalities["municipality_id"].isin(df_existing["municipality_id"])
                                  ])
    df_missing.crs = df_municipalities.crs
    df_missing = df_missing[["municipality_id", "geometry"]]

    print("Imputing %d spatial types by distance..." % len(df_missing))
    coordinates = np.vstack([df_existing["geometry"].centroid.x, df_existing["geometry"].centroid.y]).T
    kd_tree = KDTree(coordinates)

    coordinates = np.vstack([df_missing["geometry"].centroid.x, df_missing["geometry"].centroid.y]).T
    indices = kd_tree.query(coordinates, return_distance=False).flatten()

    df_missing.loc[:, "municipality_type"] = df_existing.iloc[indices]["municipality_type"].values
    df_missing.loc[:, "imputed_municipality_type"] = True
    df_missing = df_missing[["municipality_id", "municipality_type", "imputed_municipality_type", "geometry"]]

    df_mapping = pd.concat((df_existing, df_missing))

    assert (len(df_mapping) == len(df_municipalities))
    assert (set(np.unique(df_mapping["municipality_id"])) == set(np.unique(df_municipalities["municipality_id"])))

    df_mapping = pd.DataFrame(df_mapping[["municipality_id", "municipality_type", "imputed_municipality_type"]])
    df_mapping["municipality_type"] = df_mapping["municipality_type"].astype("category")

    return df_mapping

def impute_municipalities(df_points, df_zones, point_id_field, zone_id_field, fix_by_distance=True, chunk_size=10000, zone_type="", point_type=""):
    assert (type(df_points) == gpd.GeoDataFrame)
    assert (type(df_zones) == gpd.GeoDataFrame)

    assert (point_id_field in df_points.columns)
    assert (zone_id_field in df_zones.columns)
    assert (not zone_id_field in df_points.columns)

    df_original = df_points
    df_points = df_points[[point_id_field, "geometry"]]
    df_zones = df_zones[[zone_id_field, "geometry"]]

    print("Imputing %d %s zones onto %d %s points by spatial join..."
          % (len(df_zones), zone_type, len(df_points), point_type))

    result = []
    chunk_count = max(1, int(len(df_points) / chunk_size))
    for chunk in np.array_split(df_points, chunk_count):
        result.append(gpd.sjoin(df_zones, chunk, op="contains", how="right"))
    df_points = pd.concat(result).reset_index()

    if "left_index" in df_points: del df_points["left_index"]
    if "right_index" in df_points: del df_points["right_index"]

    invalid_mask = pd.isnull(df_points[zone_id_field])

    if fix_by_distance and np.any(invalid_mask):
        print("  Fixing %d points by centroid distance join..." % np.count_nonzero(invalid_mask))
        coordinates = np.vstack([df_zones["geometry"].centroid.x, df_zones["geometry"].centroid.y]).T
        kd_tree = KDTree(coordinates)

        df_missing = df_points[invalid_mask]
        coordinates = np.vstack([df_missing["geometry"].centroid.x, df_missing["geometry"].centroid.y]).T
        #indices = kd_tree.query(coordinates, return_distance=False).flatten()
        indices = [random.randrange(len(df_zones)) for i in range(len(coordinates))]

        df_points.loc[invalid_mask, zone_id_field] = df_zones.iloc[indices][zone_id_field].values

    return pd.merge(df_original, df_points[[point_id_field, zone_id_field]], on=point_id_field, how="left")
    


def impute_mun_types(df, df_municipality_types, remove_unknown=False):
    assert ("municipality_id" in df.columns)
    df = pd.merge(df, df_municipality_types, on="municipality_id")

    if remove_unknown:
        return df[~np.isnan(df["municipality_type"])]
    else:
        return df

def to_gpd(df, x="x", y="y", crs="epsg:2056", coord_type=""):
    df["geometry"] = [ geo.Point(*coord) for coord in zip(df[x], df[y])]
    df = gpd.GeoDataFrame(df)
    df.crs = crs

    if not crs == "epsg:2056":
        df = df.to_crs("epsg:2056")
        df.crs = "epsg:2056"

    return df


def impute_everything(df_mz_hhl):
    df_spatial = df_mz_hhl[["Household_id", "home_x", "home_y"]]
    print(df_spatial.head())
    #df_spatial = to_gpd(df_spatial, x = "home_x", y = "home_y", crs = "epsg:21781")
    #gdf = gpd.GeoDataFrame(df_spatial, crs = "epsg:2056")
    #gdf.to_file("Homes.shp")

    df_municipalities =  create_df_municipalities()[0]
    #df_zones = context.stage("data.spatial.zones")
    df_municipality_types = municipality_types(df_municipalities)

    #df_spatial = pd.DataFrame(df_mz_households[["person_id", "home_x", "home_y"]])
    df_spatial = to_gpd(df_spatial, "home_x", "home_y", crs = "epsg:21781")
    df_spatial = impute_municipalities(df_spatial, df_municipalities, "Household_id", "municipality_id")

    print(df_spatial.groupby(["municipality_id"]).count())
    #df_spatial = data.spatial.zones.impute(df_spatial, df_zones)
    df_spatial = impute_mun_types(df_spatial, df_municipality_types)

    df_mz_households = pd.merge(
        df_mz_hhl, df_spatial[["Household_id", "municipality_type"]],
        on="Household_id"
    )

    return df_mz_households

