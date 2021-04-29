####用于画站点图

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import csv

#解决中文显示问题
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

filepath = "D:\\data\\wind\\hail_wind.csv"
with open(filepath) as f:
    reader = csv.reader(f)
    header_row = next(reader)
    #print(header_row)
    lon = []
    lat = []
    sta_times = []
    for line in reader:
        lon.append(float(line[0]))
        lat.append(float(line[1]))
        sta_times.append(float(line[2]))
    #print('sta_times = ',sta_times)

#fig=plt.subplots()
volume = [i*20 for i in sta_times[:]]#将点放大，显示出来好看

# 设置基本图片画板
fig = plt.figure(figsize=(10, 8))

#设置地图显示经纬度范围
mapproj = Basemap(projection='cyl',
                  llcrnrlat=24.5,urcrnrlat=29.5,
                  llcrnrlon=103,urcrnrlon=110.5) 
mapproj.drawcounties()
mapproj.drawmapboundary()
#读shp文件，注意不要把后缀.shp写出来
mapproj.readshapefile("D:\\map\\guizhoushp\\Guizhou_city",'states',drawbounds=True)

#根据经纬度画点，s为点的大小，这里为动态的大小，数值大的点就大，marker是形状
#cmap是颜色
plt.scatter(lon,lat,s=volume,c=sta_times,marker='o',cmap='cool',alpha=0.8) 
plt.title('频次空间分布')

#画色标，orientation表示色标竖直还是水平，pad表示色标离图形的距离，shrink表示色标的长短
#extend表示色标两头的箭头，‘max’是从小到大，‘min’是从大到小
cbar=plt.colorbar(orientation='horizontal',pad=0.02,shrink=0.8,
                 ticks=[0,2,4,6,8,10,12,14,16],extend='max')

#cbar=plt.colorbar(orientation='horizontal',pad=0.02,ticks=[0,1,2],
#                  shrink=0.8,extend='max')

#为色标加标注
cbar.set_label('频次',size=10)

cbar.ax.tick_params(labelsize=10)
#存图
plt.savefig('D:\\data\\wind\\ss\\hail_wind sta.png')
#plt.savefig('D:\\data\\wind\\pic\\hail_wind sta.eps')
plt.show()
