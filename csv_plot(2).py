import pandas as pd
import matplotlib.pyplot as plt

class ploting():
    def __init__(self, file_path, time_col):
        df = pd.read_csv(file_path)
        df[time_col] = pd.to_datetime(df[time_col], errors='coerce')
        df = df.dropna(subset=[time_col])
        df['time'] = df[time_col]
        df = df.set_index(time_col, drop=True)
        df = df.resample('1min').min()
        index = df['id'].notnull()
        df = df[index]
        df.to_csv(r'data.csv')
        self.df = df

    def run(self):
        print(self.df)
        self.df.to_csv('data2.csv')
        self.figure()

    def figure(self):
        plt.plot(self.df['time'], self.df['device_val'], color='r')
        plt.show()


file_path = 'BBBBBB.csv'
time_col = 'create_time'
Plot = ploting(file_path, time_col)
Plot.run()

