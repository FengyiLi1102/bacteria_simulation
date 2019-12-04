import numpy as np
from matplotlib import cm
from matplotlib.ticker import LinearLocator,FormatStrFormatter
import scipy as sp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from scipy.interpolate import griddata


# Import data from local csv
data = pd.read_csv(r'Data_10_10_0.05.csv')

# Set x, y, z data
x = data.loc[:40, 'N']
y = data.loc[:40, 'd']
z = data.loc[:40, 'mean']

xyz = {'x': x, 'y': y, 'z': z}

# put the data into a pandas DataFrame
df = pd.DataFrame(xyz, index=range(len(xyz['x']))) 

# re-create the 2D-arrays
x1 = np.linspace(df['x'].min(), df['x'].max(), len(df['x'].unique()))
y1 = np.linspace(df['y'].min(), df['y'].max(), len(df['y'].unique()))
x2, y2 = np.meshgrid(x1, y1)
z2 = griddata((df['x'], df['y']), df['z'], (x2, y2), method='cubic')

fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(x2, y2, z2, rstride=1, cstride=1,
                       linewidth=0, antialiased=False)
ax.set_zlim(0, 4)

ax.set_xlabel('N / strip')
ax.set_ylabel('d / unit')
ax.set_zlabel('T_1/2 / step')

ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

fig.colorbar(surf, shrink=0.5, aspect=5)
plt.title('T_1/2 with N, d and d2 combinations')

# plt.show()
