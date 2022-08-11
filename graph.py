import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pd.read_csv('QuickMill_out.csv')
df["Timestamp"] = pd.to_datetime(df["Timestamp"])
df = df.set_index("Timestamp")
df.plot()
dtFmt = mdates.DateFormatter("%H:%M:%S") # define the formatting
plt.gca().xaxis.set_major_formatter(dtFmt)
plt.xticks(rotation = 45)
plt.ylabel("Amplitude")
plt.xlabel("Time")
plt.show()

