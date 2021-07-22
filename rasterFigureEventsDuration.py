import random
import matplotlib.pyplot as plt
import pandas as pd
plt.ion()

allDat = []
for i in range(10):
    var1 = random.sample(range(1, 1000), 20)
    var1.sort()
    var2 = [random.randint(1, 20) for x in range(20)]
    dat = pd.DataFrame({'frame': var1, 'duration': var2})
    dat['trial'] = i
    allDat.append(dat)
allDat = pd.concat(allDat)

for i,j in allDat.iterrows():
    # print(i,j)
    plt.hlines(y = j['trial'], xmin = j['frame'], xmax = j['frame']+j['duration'], alpha=0.3, linewidth=22)

plt.ylim(-1,10)
plt.xlabel('time')
plt.ylabel('Trials // events duration')
plt.savefig(r'Y:\git\rumLab\dataVizPy\raster.svg')