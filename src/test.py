# -*- coding: UTF-8 -*-

from gdalconst import *
from osgeo import gdal
import numpy as np


def read_info(filename):
    dataset = gdal.Open(filename, GA_ReadOnly)  # 打开文件
    im_width = dataset.RasterXSize  # 栅格矩阵的列数
    im_height = dataset.RasterYSize  # 栅格矩阵的行数
    im_geotrans = dataset.GetGeoTransform()  # 仿射矩阵
    im_proj = dataset.GetProjection()  # 地图投影信息
    return im_proj, im_geotrans, im_height, im_width


def read_value(filename):
    dataset = gdal.Open(filename, GA_ReadOnly)  # 打开文件
    im_width = dataset.RasterXSize  # 栅格矩阵的列数
    im_height = dataset.RasterYSize  # 栅格矩阵的行数
    im_geotrans = dataset.GetGeoTransform()  # 仿射矩阵
    im_proj = dataset.GetProjection()  # 地图投影信息
    im_data = dataset.ReadAsArray(0, 0, im_width, im_height).astype(
        np.float)  # 将数据写成数组，对应栅格矩阵
    print(filename, im_proj, im_geotrans, im_data.shape)
    return im_data


def write_img(filename, im_proj, im_geotrans, im_data):
    # gdal数据类型包括
    # gdal.GDT_Byte,
    # gdal .GDT_UInt16, gdal.GDT_Int16, gdal.GDT_UInt32, gdal.GDT_Int32,
    # gdal.GDT_Float32, gdal.GDT_Float64

    # 判断栅格数据的数据类型
    if 'int8' in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float32

    # 判读数组维数
    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    else:
        im_bands, (im_height, im_width) = 1, im_data.shape

    # for i in range(0, im_height):
    #     for j in range(0, im_width):
    #         if im_data[i, j] != -9999.0:
    #             print(im_data[i, j])

    # 创建文件
    driver = gdal.GetDriverByName("GTiff")  # 数据类型必须有，因为要计算需要多大内存空间
    dataset = driver.Create(filename, im_width, im_height, im_bands, datatype)

    dataset.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
    dataset.SetProjection(im_proj)  # 写入投影

    if im_bands == 1:
        dataset.GetRasterBand(1).WriteArray(im_data)  # 写入数组数据
    else:
        for i in range(im_bands):
            dataset.GetRasterBand(i + 1).WriteArray(im_data[i])
    del dataset


if __name__ == '__main__':
    proj, geotrans, row, column = read_info('002.tif')  # 读数据

    filesum = [[0.0]*column]*row
    average = [[0.0]*column]*row
    filesum = np.array(filesum)
    average = np.array(average)

    np.add(filesum, read_value('002.tif'), filesum)
    # np.add(filesum, read_value('003.tif'), filesum)

    for i in range(0, row):
        for j in range(0, column):
            average[i, j] = filesum[i, j]*1.0/1
            if average[i, j] < 0:
                average[i, j] = 0

    write_img(r'average.tif', proj, geotrans, average)  # 写数据
