# -*- coding: UTF-8 -*-

import os
import os.path
import gdal
import sys
from gdalconst import *
from osgeo import gdal
import osr
import numpy as np


def WriteGTiffFile(filename, nRows, nCols, data, geotrans, proj, noDataValue, gdalType):  # 向磁盘写入结果文件
    format = "GTiff"
    driver = gdal.GetDriverByName(format)
    ds = driver.Create(filename, nCols, nRows, 1, gdalType)
    ds.SetGeoTransform(geotrans)
    ds.SetProjection(proj)
    ds.GetRasterBand(1).SetNoDataValue(noDataValue)
    ds.GetRasterBand(1).WriteArray(data)
    ds = None


def File():  # 遍历文件，读取数据，算出均值
    rows, cols, geotransform, projection, noDataValue = Readxy(
        '002.tif')
    # 获取源文件的行，列，投影等信息，所有的源文件这些信息都是一致的
    print('rows and cols is ', rows, cols)
    filesum = [[0.0]*cols]*rows  # 栅格值和，二维数组
    average = [[0.0]*cols]*rows  # 存放平均值，二维数组
    filesum = np.array(filesum)  # 转换类型为np.array
    average = np.array(average)
    print('the type of filesum', type(filesum))
    count = 0
    rootdir = '.'
    for dirpath, filename, filenames in os.walk(rootdir):  # 遍历源文件
        for filename in filenames:
            if os.path.splitext(filename)[1] == '.tif':  # 判断是否为tif格式
                filepath = os.path.join(dirpath, filename)
                # 获得除去扩展名的文件名，比如201013.tif，purename为201013
                purename = filename.replace('.tif', '')
                # if purename[:4] == '2010':  # 判断年份
                filedata = [[0.0]*cols]*rows
                filedata = np.array(filedata)
                filedata = Read(filepath)  # 将2010年的13幅图像数据存入filedata中
                count += 1
                np.add(filesum, filedata, filesum)  # 求13幅图像相应栅格值的和
                # print str(count)+'this is filedata',filedata
    print('count is ', count)
    for i in range(0, rows):
        for j in range(0, cols):
            if(filesum[i, j] == noDataValue*count):  # 处理图像中的noData
                average[i, j] = -9999
            else:
                average[i, j] = filesum[i, j]*1.0/count  # 求平均
    WriteGTiffFile("all.tif", rows, cols, average,
                   geotransform, projection, -9999, GDT_Float32)  # 写入结果文件


def Readxy(RasterFile):  # 读取每个图像的信息
    ds = gdal.Open(RasterFile, GA_ReadOnly)
    if ds is None:
        print('Cannot open ', RasterFile)
        sys.exit(1)
    cols = ds.RasterXSize
    rows = ds.RasterYSize
    band = ds.GetRasterBand(1)
    data = band.ReadAsArray(0, 0, cols, rows)
    noDataValue = band.GetNoDataValue()
    projection = ds.GetProjection()
    geotransform = ds.GetGeoTransform()
    print(cols, rows, band, noDataValue, projection, geotransform)
    return rows, cols, geotransform, projection, noDataValue


def Read(RasterFile):  # 读取每个图像的信息
    ds = gdal.Open(RasterFile, GA_ReadOnly)
    if ds is None:
        print('Cannot open ', RasterFile)
        sys.exit(1)
    cols = ds.RasterXSize
    rows = ds.RasterYSize
    band = ds.GetRasterBand(1)
    data = band.ReadAsArray(0, 0, cols, rows)
    return data


if __name__ == "__main__":
    print("ok1")
    File()
    print("ok2")
