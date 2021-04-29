# -*- coding: UTF-8 -*-

import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import matplotlib as mpl
import matplotlib.colors as colors
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

# ################################### BEGIN ###################################
ds = pygrib.open('W_NAFP_C_ECMF_20210418193848_P_C3E04181200050212001-ACHN')

for i in list(range(0, 5)):
    pre = ds.select(name='Total precipitation')[i]
    # 裁剪数据并将值单位换算为mm
    data = pre.data()[0]*1000

    # 计算平均值
    if 'avg' in vars():
        avg = np.average(np.array([avg, data]), axis=0)
    else:
        avg = data

# 裁剪经纬度数据
lats = pre.data()[1][:, 0]
lons = pre.data()[2][0, :]
# 网格化 ，生成网格点坐标矩阵
lons, lats = np.meshgrid(lons, lats)

# 自定义颜色数值区间列表
clevs = [0.1, 10., 25., 50., 100., 250.]
# 自定义数值区间颜色列表
cdict = ['#FFFFFF', '#A9F090', '#40B73F',
         '#63B7FF', '#0000FE', '#FF00FC', '#850042']
# 自定义颜色映射 color-map
cmap = colors.ListedColormap(cdict[1:])
# 基于离散区间生成颜色映射索引
norm = mpl.colors.BoundaryNorm(clevs, len(clevs) - 1)

# 绘制等值线、等值线填色
cf = ax.contourf(lons, lats, avg, clevs, cmap=cmap,
                 norm=norm, extend='both', transform=proj)
cf.cmap.set_under(cdict[0])

# 添加色标图
plt.colorbar(cf, ax=ax, ticks=clevs, extendfrac='auto',
             aspect=14, format='%3.1f', shrink=.95, fraction=0.03, pad=0.04)

# # 站点经纬度
# nameandstation = {'湘潭市': {'valueOffset': [-0.12, 0], 'nameOffset': [-0.4, -0.2], 'lonlat': [112.951614, 27.835959]}, '常德市': {'valueOffset': [0, 0], 'nameOffset': [-0.1, 0.2], 'lonlat': [111.70473, 29.037876]}, '永州市': {'valueOffset': [0, 0], 'nameOffset': [-0.1, -0.2], 'lonlat': [111.620029, 26.427676]}, '岳阳市': {'valueOffset': [0, 0], 'nameOffset': [-0.1, -0.2], 'lonlat': [113.135488, 29.362925]}, '张家界市': {'valueOffset': [0, 0], 'nameOffset': [-0.12, 0.2], 'lonlat': [110.485532, 29.123574]}, '湘西州': {'valueOffset': [0, 0], 'nameOffset': [-0.1, 0.2], 'lonlat': [109.704449, 28.267493]}, '郴州市': {'valueOffset': [0, 0], 'nameOffset': [-0.1, 0.2], 'lonlat': [113.021458, 25.777984]}, '长沙市': {'valueOffset': [0, 0], 'nameOffset': [0.25, 0], 'lonlat': [
#     112.94662, 28.235654]}, '衡阳市': {'valueOffset': [0, 0], 'nameOffset': [-0.1, -0.2], 'lonlat': [112.578449, 26.901379]}, '益阳市': {'valueOffset': [0, 0], 'nameOffset': [-0.4, -0.1], 'lonlat': [112.360942, 28.560473]}, '邵阳市': {'valueOffset': [0, 0], 'nameOffset': [-0.4, 0], 'lonlat': [111.474432, 27.246556]}, '怀化市': {'valueOffset': [-0.1, -0.2], 'nameOffset': [0, 0], 'lonlat': [110.008514, 27.575929]}, '株洲市': {'valueOffset': [0.02, 0], 'nameOffset': [-0.05, -0.2], 'lonlat': [113.142199, 27.833824]}, '娄底市': {'valueOffset': [-0.18, 0], 'nameOffset': [-0.03, -0.2], 'lonlat': [112.002653, 27.703976]}}

# # 绘制城市名
# for k, v in nameandstation.items():
#     station = nameandstation[k]
#     ax.text(station['lonlat'][0]+station['nameOffset'][0],
#             station['lonlat'][1]+station['nameOffset'][1], k, fontsize=9, c='k')

# 添加标题
plt.title('W_NAFP_C_ECMF_20210418193848_P_C3E04181200050212001-ACHN\nTotal precipitation ens 前五维度平均值')

# 显示绘图结果
plt.show()
