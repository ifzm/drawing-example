# -*- coding: UTF-8 -*-

import time
import sys
import os
import numpy as np
from scipy.stats import pearsonr

start_time = time.perf_counter()

# 读取文件数据
a = np.fromfile(
    './Z_NWGD_C_BECS_20200409070000_DLYB_RQPF_MOSAIC_1km_F060.bin', 'float32')
b = np.fromfile(
    './Z_NWGD_C_BECS_20200721000000_DLYB_RQPF_MOSAIC_1km_F030.bin', 'float32')

# 计算皮尔逊系数
print(pearsonr(a, b))

# 输出:(r, p)
# r:相关系数[-1，1]之间
# p:p值越小

stop_time = time.perf_counter()

print("%s cost %s second" %
      (os.path.basename(sys.argv[0]), stop_time - start_time))
