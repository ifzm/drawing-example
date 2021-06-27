# -*- coding: UTF-8 -*-

import datetime
import numpy as np
import pandas as pd
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

plt.rcParams['font.sans-serif'] = ['SimHei']
fig = plt.figure(figsize=(9, 9))

# 读取 shp
fname = './shp/hunan/HnCityRegion.shp'
adm1_shapes = list(shpreader.Reader(fname).geometries())

# 站点经纬度
nameandstation = {'湘潭市': {'valueOffset': [-0.12, 0], 'nameOffset': [-0.4, -0.2], 'lonlat': [112.951614, 27.835959]}, '常德市': {'valueOffset': [0, 0], 'nameOffset': [-0.1, 0.2], 'lonlat': [111.70473, 29.037876]}, '永州市': {'valueOffset': [0, 0], 'nameOffset': [-0.1, -0.2], 'lonlat': [111.620029, 26.427676]}, '岳阳市': {'valueOffset': [0, 0], 'nameOffset': [-0.1, -0.2], 'lonlat': [113.135488, 29.362925]}, '张家界市': {'valueOffset': [0, 0], 'nameOffset': [-0.12, 0.2], 'lonlat': [110.485532, 29.123574]}, '湘西州': {'valueOffset': [0, 0], 'nameOffset': [-0.1, 0.2], 'lonlat': [109.704449, 28.267493]}, '郴州市': {'valueOffset': [0, 0], 'nameOffset': [-0.1, 0.2], 'lonlat': [113.021458, 25.777984]}, '长沙市': {'valueOffset': [0, 0], 'nameOffset': [0.25, 0], 'lonlat': [
    112.94662, 28.235654]}, '衡阳市': {'valueOffset': [0, 0], 'nameOffset': [-0.1, -0.2], 'lonlat': [112.578449, 26.901379]}, '益阳市': {'valueOffset': [0, 0], 'nameOffset': [-0.4, -0.1], 'lonlat': [112.360942, 28.560473]}, '邵阳市': {'valueOffset': [0, 0], 'nameOffset': [-0.4, 0], 'lonlat': [111.474432, 27.246556]}, '怀化市': {'valueOffset': [-0.1, -0.2], 'nameOffset': [0, 0], 'lonlat': [110.008514, 27.575929]}, '株洲市': {'valueOffset': [0.02, 0], 'nameOffset': [-0.05, -0.2], 'lonlat': [113.142199, 27.833824]}, '娄底市': {'valueOffset': [-0.18, 0], 'nameOffset': [-0.03, -0.2], 'lonlat': [112.002653, 27.703976]}}
# 等级颜色
namendlevel = {'优': '#6EC128', '良': '#DFCB3A', '轻度污染': '#FB5E28',
               '中度污染': '#E50424', '重度污染': '#851054', '严重污染': '#3E0856'}

# 创建图例色块
rects = []
for key, value in namendlevel.items():
    rects.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=value))

# 读取数据
df = pd.read_excel('./data/2020-12-air.xls', sheet_name='Sheet1')

# 获取最大行，最大列
nrows = df.shape[0]
ncols = df.columns.size

# 构建数据集
data = {}
for iRow in range(nrows):
    for iCol in range(ncols):
        value = df.iloc[iRow, iCol]
        if iCol == 0:
            city = value
        else:
            day = '2020-' + df.columns[iCol].replace(' ', '').replace('/', '-')
            if day not in data:
                data[day] = {}
            data[day][city] = value

# print(data)


def calcLevel(value):
    # 0至50优 51至100良 101至150轻度污染 151至200中度污染 201至300重度污染 301至500严重污染
    if 0 <= value <= 50:
        return namendlevel['优']
    if 50 < value <= 100:
        return namendlevel['良']
    if 100 < value <= 150:
        return namendlevel['轻度污染']
    if 150 < value <= 200:
        return namendlevel['中度污染']
    if 200 < value <= 300:
        return namendlevel['重度污染']
    if 300 < value <= 500:
        return namendlevel['严重污染']
    return namendlevel['严重污染']


# 遍历数据集
for key, value in data.items():
    ax = plt.axes(projection=ccrs.PlateCarree())

    # --添加标题
    title = f'湖南省空气质量等级和 AQI 城市站点分布图（' + key + '）'
    ax.set_title(title, fontsize=16)

    # 添加 shp
    ax.add_geometries(adm1_shapes, ccrs.PlateCarree(),
                      edgecolor='black', facecolor='white', alpha=0.5)

    # 添加图例
    ax.legend(rects, namendlevel.keys(), title='AQI:无量纲\n空气质量等级',
              loc='lower left', fancybox=False, frameon=False)

    # 添加网格线标注
    ax.grid(linestyle=':', color='black', linewidth=0)
    ax.set_extent([108.5, 114.5, 24.5, 30.25])
    ax.set_xticks(np.arange(108.5, 114.5, 1), crs=ccrs.PlateCarree())
    ax.set_yticks(np.arange(24.5, 30.25, 1), crs=ccrs.PlateCarree())
    # 添加经纬度格式化文本 °E/°N ...
    lon_formatter = LongitudeFormatter(zero_direction_label=False)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    # 绘制数值与城市名
    for k, v in value.items():
        station = nameandstation[k]
        ax.text(station['lonlat'][0]+station['valueOffset'][0], station['lonlat'][1]+station['valueOffset'][1], v, fontsize=10, c='white', bbox=dict(
            facecolor=calcLevel(v), alpha=1, boxstyle='round'))
        ax.text(station['lonlat'][0]+station['nameOffset'][0],
                station['lonlat'][1]+station['nameOffset'][1], k, fontsize=9, c='k')

    # 保存图片
    plt.savefig('./images/' + title + '.jpg')
    # 清空画布
    plt.clf()

# # plt.show()
