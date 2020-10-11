#Basic analysis of time series rainfall data in Auckland between 1872 and 1997
import sys
import numpy as np
import pandas as pd
from pandas import datetime

class RainFall:

    def __init__(self,inputfile):
        self.inputfile = inputfile

    def read_input(self):
        try:
            with open(self.inputfile, 'r') as input_file:
                 self.input_data = pd.read_csv(self.inputfile,
                                 skiprows=3,
                                 header=None,
                                 names=['timestamp','rain_value', 'grade', 'interpol_type', 'event_timestamp'],
                                 parse_dates=['timestamp'],
                                 index_col='timestamp')
                 return self.input_data
        except IOError:
                print("File not found or path is incorrect")
                sys.exit()

    def clean_data(self):
        row_number=self.input_data.shape[0]
        print('Number of rows:', row_number)
        print(self.input_data.describe())
        self.new_df=self.input_data.drop(columns=['event_timestamp', 'grade', 'interpol_type'])
        return self.new_df

    def data_stats(self):
        print('Basic statistics:', '\n')

        start=min(self.new_df.index)
        end=max(self.new_df.index)
        print('Start date:', start, '--- End date:', end)
        unique_date=len(self.new_df.index.unique())
        day_num=self.new_df.shape[0]
        print('Number of measurements:', day_num)
        print('Number of unique days:', unique_date)

        delta=max(self.new_df.index)-min(self.new_df.index)
        print('Number of days between the first and last measurements:',  delta.days)
        print('Number of days with no measurements:', (delta.days-day_num), '\n')

        rain_days= self.new_df['rain_value'].value_counts(dropna=True, sort=True)
        print('Number of days with no rain:', rain_days[0], '---', round(rain_days[0]/day_num *100, 0),'%')

        y=list(filter(lambda x: x <= 1, rain_days.index))
        little_rain=rain_days.values[0:14].sum()
        print('Number of days with rain, less than 1mm/day:', little_rain, '---', round(little_rain/day_num*100, 0), '%', '\n')

        df_sorted=self.new_df.sort_values(by='rain_value', ascending=False)
        print('Dates with the maximum rain falls:','\n')
        print(df_sorted.head(5))


def main():
   filename='Data/AucklandRainfall1872-1997.csv'
   print('Reading file ', filename, '...\n')

   rain_data=RainFall(filename)
   df = rain_data.read_input()
   print(df.head(5))

   #Cleaning data
   print('Dropping unnecessary columns...')
   new_df=rain_data.clean_data()
   print(new_df.head(5), '\n')

   #Data stats
   rain_data.data_stats()


if __name__=="__main__":
    main()
