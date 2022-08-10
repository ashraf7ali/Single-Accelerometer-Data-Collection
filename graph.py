import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('QuickMill_out.csv')

df.plot()
# df.plot(kind = 'scatter', x = 'Timestamp', y = 'Aplitude')
plt.show()
print(df.head()) 