import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv("C:/Users/Maartje/Documents/studeren/jaar 3/bpp/species.csv")
df = df.dropna() # Drop the "no hits" line
df['A'] = np.random.rand(len(df)) * 100 + 1

# Do the summing to get the values for each layer
def nested_pie(df):

    cols = df.columns.tolist()
    outd = {}
    gb = df.groupby(cols[0], sort=False).sum()
    outd[0] = {'names':gb.index.values, 'values':gb.values}
    for lev in range(1,7):
        gb = df.groupby(cols[:(lev+1)], sort=False).sum()
        outd[lev] = {'names':gb.index.levels[lev][gb.index.labels[lev]].tolist(),
                     'values':gb.values}
    return outd6

outd = nested_pie(df)
diff = 1/7.0

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

# This first pie chart fill the plot, it's the lowest level
plt.pie(outd[6]['values'], labels=outd[6]['names'], labeldistance=0.9,
        colors=colors)

ax = plt.gca()


# For each successive plot, change the max radius so that they overlay
for i in np.arange(5,-1,-1):
    ax.pie(outd[i]['values'], labels=outd[i]['names'],
           radius=np.float(i+1)/7.0, labeldistance=((2*(i+1)-1)/14.0)/((i+1)/7.0), colors=colors)

ax.set_aspect('equal')

plt.show()



