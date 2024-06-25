import cv2
import numpy as np
from osgeo import gdal



# Load DTM data
def load_dtm(filepath):
    ds = gdal.Open(filepath)
    band = ds.GetRasterBand(1)
    dtm_data = band.ReadAsArray()
    return dtm_data


# Generate a grid for the mesh
def generate_grid(dtm_data):
    x = np.linspace(0, dtm_data.shape[1], dtm_data.shape[1])
    y = np.linspace(0, dtm_data.shape[0], dtm_data.shape[0])
    x, y = np.meshgrid(x, y)
    z = dtm_data
    z = np.maximum(z, 0)
    return x, y, z


def preprocess_terrain_data(dtm_filepath, image_filepath):
    dtm_data = load_dtm(dtm_filepath)
    dtm_grid = generate_grid(dtm_data)
    orthophoto = cv2.imread(image_filepath)
    return orthophoto, dtm_grid
