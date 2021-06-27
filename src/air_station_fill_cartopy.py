# -*- coding: UTF-8 -*-

import numpy as np
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import ListedColormap
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter

plt.rcParams['font.sans-serif'] = ['SimHei']
fig = plt.figure(figsize=(9, 9))

# 读取 shp
fname = './shp/hunan/HnCityRegion.shp'
reader = shpreader.Reader(fname)
records = reader.records()

ax = plt.axes(projection=ccrs.PlateCarree())
# 添加网格线标注
ax.grid(linestyle=':', color='black', linewidth=0)
ax.set_extent([108.5, 114.5, 24.5, 30.25])
ax.set_xticks(np.arange(108.5, 114.5, 1), crs=ccrs.PlateCarree())
ax.set_yticks(np.arange(24.5, 30.25, 1), crs=ccrs.PlateCarree())

data = {
    "湘西土家族苗族自治州": {
        "name": "湘西土家族苗族自治州",
        "value": 1,
        "color": "#10ac50"
    },
    "怀化市": {
        "name": "怀化市",
        "value": 1,
        "color": "#10ac50"
    },
    "娄底市": {
        "name": "娄底市",
        "value": 3,
        "color": "#94d353"
    },
    "郴州市": {
        "name": "郴州市",
        "value": 4,
        "color": "#94d353"
    },
    "岳阳市": {
        "name": "岳阳市",
        "value": 6,
        "color": "#c6d22f"
    },
    "张家界市": {
        "name": "张家界市",
        "value": 7,
        "color": "#c6d22f"
    },
    "永州市": {
        "name": "永州市",
        "value": 10,
        "color": "#b8b804"
    },
    "益阳市": {
        "name": "益阳市",
        "value": 18,
        "color": "#fbd10a"
    },
    "衡阳市": {
        "name": "衡阳市",
        "value": 19,
        "color": "#fbd10a"
    },
    "株洲市": {
        "name": "株洲市",
        "value": 21,
        "color": "#fa6506"
    },
    "常德市": {
        "name": "常德市",
        "value": 21,
        "color": "#fa6506"
    },
    "长沙市": {
        "name": "长沙市",
        "value": 26,
        "color": "#fa6506"
    },
    "湘潭市": {
        "name": "湘潭市",
        "value": 26,
        "color": "#fa6506"
    },
    "邵阳市": {
        "name": "邵阳市",
        "value": 31,
        "color": "#e22c0b"
    }
}

for record in records:
    ax.add_geometries([record.geometry], ccrs.PlateCarree(),
                      edgecolor='w', facecolor=data[record.attributes['NAME']]['color'], alpha=1)

cmap = mpl.cm.Spectral_r
newcolors = cmap(np.linspace(0, 1, 256))
newcmap = ListedColormap(newcolors[:200])

norm = mpl.colors.Normalize(vmin=0, vmax=31)
m = mpl.cm.ScalarMappable(cmap=newcmap, norm=norm)
m.set_array([0, 5, 10, 15, 20, 25, 31])
plt.colorbar(ax, ticks=[0, 5, 10, 15, 20, 25, 31],
             aspect=14, shrink=.95, fraction=0.05, pad=0.04)

# ax3 = fig.add_axes([0.3, 0.2, 0.2, 0.5])
# cmap = mpl.cm.Spectral_r
# norm = mpl.colors.Normalize(vmin=1, vmax=31)
# cb3 = mpl.colorbar.ColorbarBase(ax3, cmap=cmap,
#                                 norm=norm,
#                                 extend='both',
#                                 spacing='proportional',
#                                 orientation='vertical')

# 站点经纬度
nameandstation = {'湘潭市': {'valueOffset': [-0.12, 0], 'nameOffset': [-0.4, -0.2], 'lonlat': [112.951614, 27.835959]}, '常德市': {'valueOffset': [0, 0], 'nameOffset': [-0.1, 0.2], 'lonlat': [111.70473, 29.037876]}, '永州市': {'valueOffset': [0, 0], 'nameOffset': [-0.1, -0.2], 'lonlat': [111.620029, 26.427676]}, '岳阳市': {'valueOffset': [0, 0], 'nameOffset': [-0.1, -0.2], 'lonlat': [113.135488, 29.362925]}, '张家界市': {'valueOffset': [0, 0], 'nameOffset': [-0.12, 0.2], 'lonlat': [110.485532, 29.123574]}, '湘西州': {'valueOffset': [0, 0], 'nameOffset': [-0.1, 0.2], 'lonlat': [109.704449, 28.267493]}, '郴州市': {'valueOffset': [0, 0], 'nameOffset': [-0.1, 0.2], 'lonlat': [113.021458, 25.777984]}, '长沙市': {'valueOffset': [0, 0], 'nameOffset': [0.25, 0], 'lonlat': [
    112.94662, 28.235654]}, '衡阳市': {'valueOffset': [0, 0], 'nameOffset': [-0.1, -0.2], 'lonlat': [112.578449, 26.901379]}, '益阳市': {'valueOffset': [0, 0], 'nameOffset': [-0.4, -0.1], 'lonlat': [112.360942, 28.560473]}, '邵阳市': {'valueOffset': [0, 0], 'nameOffset': [-0.4, 0], 'lonlat': [111.474432, 27.246556]}, '怀化市': {'valueOffset': [-0.1, -0.2], 'nameOffset': [0, 0], 'lonlat': [110.008514, 27.575929]}, '株洲市': {'valueOffset': [0.02, 0], 'nameOffset': [-0.05, -0.2], 'lonlat': [113.142199, 27.833824]}, '娄底市': {'valueOffset': [-0.18, 0], 'nameOffset': [-0.03, -0.2], 'lonlat': [112.002653, 27.703976]}}

# 绘制城市名
for k, v in nameandstation.items():
    station = nameandstation[k]
    ax.text(station['lonlat'][0]+station['nameOffset'][0],
            station['lonlat'][1]+station['nameOffset'][1], k, fontsize=9, c='k')

plt.show()
