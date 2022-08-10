import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('QuickMill_out.csv')
df = df.set_index("Timestamp")

df.plot()
dtFmt = mdates.DateFormatter('%Y-%m-%d') # define the formatting
plt.gca().xaxis.set_major_formatter(dtFmt)
plt.xticks(rotation = 45)
plt.show()
