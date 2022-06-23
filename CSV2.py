import pandas as pd

class ploting():
    def __init__(self, file_path, time_col):
        df = pd.read_csv(file_path)
        df[time_col] = pd.to_datetime(df[time_col], errors='coerce')
        df['id'] = pd.to_numeric(df['id'], errors='coerce')
        df = df.dropna(subset=['id'])
        df = df.set_index(time_col, drop=True)
        df = df.resample('1min').min()
        index = df['id'].notnull()
        df = df[index]
        df.to_csv(r'data.csv')
        self.df = df

    def run(self):
        #print(self.df)
        self.df.to_csv('data2.csv')


'''''
file_path = 'BBBBBB.csv'
time_col = 'create_time'
Plot = ploting(file_path, time_col)
Plot.run()
'''''
