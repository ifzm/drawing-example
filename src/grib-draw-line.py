# -*- coding: UTF-8 -*-

import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
import numpy as np
import pygrib
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
# 创建画布
fig = plt.figure(figsize=(9, 9))

# 定义投影
proj = ccrs.PlateCarree()

# 读取 shp
# fname = './shp/HnCityRegion.shp'
fname = './china/bou1_4l.shp'
adm1_shapes = list(shpreader.Reader(fname).geometries())
ax = plt.axes(projection=proj)
ax.add_geometries(adm1_shapes, proj,
                  edgecolor='k', facecolor='none', alpha=1)

# 添加网格线标注
ax.grid(linestyle=':', color='k', linewidth=0)
# ax.set_extent([108.5, 114.5, 24.5, 30.25])
# ax.set_xticks(np.arange(108.5, 114.5, 1), crs=proj)
# ax.set_yticks(np.arange(24.5, 30.25, 1), crs=proj)
ax.set_extent([70, 140, 15, 55])
ax.set_xticks(np.arange(70, 140, 7), crs=proj)
ax.set_yticks(np.arange(15, 55, 5), crs=proj)

# 添加经纬度格式化文本 °E/°N ...
lon_formatter = LongitudeFormatter(zero_direction_label=False)
lat_formatter = LatitudeFormatter()
ax.xaxis.set_major_formatter(lon_formatter)
ax.yaxis.set_major_formatter(lat_formatter)

# # 站点经纬度
# nameandstation = {'湘潭市': {'valueOffset': [-0.12, 0], 'nameOffset': [-0.4, -0.2], 'lonlat': [112.951614, 27.835959]}, '常德市': {'valueOffset': [0, 0], 'nameOffset': [-0.1, 0.2], 'lonlat': [111.70473, 29.037876]}, '永州市': {'valueOffset': [0, 0], 'nameOffset': [-0.1, -0.2], 'lonlat': [111.620029, 26.427676]}, '岳阳市': {'valueOffset': [0, 0], 'nameOffset': [-0.1, -0.2], 'lonlat': [113.135488, 29.362925]}, '张家界市': {'valueOffset': [0, 0], 'nameOffset': [-0.12, 0.2], 'lonlat': [110.485532, 29.123574]}, '湘西州': {'valueOffset': [0, 0], 'nameOffset': [-0.1, 0.2], 'lonlat': [109.704449, 28.267493]}, '郴州市': {'valueOffset': [0, 0], 'nameOffset': [-0.1, 0.2], 'lonlat': [113.021458, 25.777984]}, '长沙市': {'valueOffset': [0, 0], 'nameOffset': [0.25, 0], 'lonlat': [
#     112.94662, 28.235654]}, '衡阳市': {'valueOffset': [0, 0], 'nameOffset': [-0.1, -0.2], 'lonlat': [112.578449, 26.901379]}, '益阳市': {'valueOffset': [0, 0], 'nameOffset': [-0.4, -0.1], 'lonlat': [112.360942, 28.560473]}, '邵阳市': {'valueOffset': [0, 0], 'nameOffset': [-0.4, 0], 'lonlat': [111.474432, 27.246556]}, '怀化市': {'valueOffset': [-0.1, -0.2], 'nameOffset': [0, 0], 'lonlat': [110.008514, 27.575929]}, '株洲市': {'valueOffset': [0.02, 0], 'nameOffset': [-0.05, -0.2], 'lonlat': [113.142199, 27.833824]}, '娄底市': {'valueOffset': [-0.18, 0], 'nameOffset': [-0.03, -0.2], 'lonlat': [112.002653, 27.703976]}}

# # 绘制城市名
# for k, v in nameandstation.items():
#     station = nameandstation[k]
#     ax.text(station['lonlat'][0]+station['nameOffset'][0],
#             station['lonlat'][1]+station['nameOffset'][1], k, fontsize=9, c='gray')

# ################################### BEGIN ###################################
ds = pygrib.open('W_NAFP_C_ECMF_20210418193848_P_C3E04181200050212001-ACHN')

colors = ['#0072BD', '#D95319', '#EDB120', '#7E2F8E', '#77AC30']
for i, c in enumerate(colors):
    hgt_500 = ds.select(name='Geopotential Height',
                        typeOfLevel='isobaricInhPa', level=500)[i]
    # 裁剪数据并将值单位换算为dagpm
    lats = hgt_500.data()[1][:, 0]
    lons = hgt_500.data()[2][0, :]
    hgt_500 = hgt_500.data()[0]*0.1

    # 网格化 ，生成网格点坐标矩阵
    lons, lats = np.meshgrid(lons, lats)

    # 等高线
    isoheight = ax.contour(lons, lats, hgt_500, transform=proj, levels=[
        580, 584, 588], colors=c, linewidths=1.2)

    # 等高线标注
    ax.clabel(isoheight, fontsize=14, colors=c, inline_spacing=6, fmt='%d')

# ################################### END ###################################

# 添加标题
plt.title('W_NAFP_C_ECMF_20210418193848_P_C3E04181200050212001-ACHN\nGeopotential Height ens 前五维度叠加')

# 显示绘图结果
plt.show()
