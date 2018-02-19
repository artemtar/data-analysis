import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')
import numpy as np

stats = {'Day':[1,2,3,4,5,6],
            'Visitors':[43,34,65,56,29,76],
            'Bounce Rate':[65,67,78,65,45,52]}

df_stats = pd.DataFrame(stats)

# print(df_stats)
# print(df_stats.head)
# print(df_stats.tail(2))

# df_stats_day = df_stats.set_index('Day')
# print(df_stats_day)

### same way

df_stats.set_index('Day', inplace=True)
print(df_stats)

print(df_stats.Visitors)
print(df_stats['Visitors'])
print(df_stats[['Visitors', 'Bounce Rate']])
df_stats['Visitors'].tolist()

array = np.array(df_stats[['Visitors', 'Bounce Rate']])
print(array)
df_array = pd.DataFrame(array)
print(df_array)