from osgeo import gdal
from gdalconst import *

input_raster = r"003.tif"
# or as an alternative if the input is already a gdal raster object you can use that gdal object
input_raster = gdal.Open(input_raster, GA_ReadOnly)
input_shape = r"china/bou1_4l.shp"  # or any other format
output_raster = r'003.mask.tif'  # your output raster file

ds = gdal.Warp(output_raster,
               input_raster,
               format='tif',
               cutlineDSName=input_shape,      # or any other file format
               # optionally you can filter your cutline (shapefile) based on attribute values
               cutlineWhere="",
               dstNodata=-9999)              # select the no data value you like

ds = None
