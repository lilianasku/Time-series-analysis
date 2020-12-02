#Basic analysis of time series rainfall data
import sys
import numpy as np
import pandas as pd
from pandas import datetime

class RainFall(object):

    def __init__(self, inputfile):
        self.inputfile = inputfile

    def read_input(self):
        try:
            with open(self.inputfile, 'r') as input_file:
                 self.input_data = pd.read_csv(self.inputfile,
                                 skiprows=3,
                                 header = None,
                                 names = ['timestamp','rain_value', 'grade', 'interpol_type', 'event_timestamp'],
                                 parse_dates = ['timestamp'],
                                 index_col = 'timestamp')
                 return self.input_data
        except IOError:
                print("File not found or path is incorrect")
                sys.exit()

    def clean_data(self):
        row_number = self.input_data.shape[0]
        print('Number of rows:', row_number)
        print(self.input_data.describe())
        self.new_df = self.input_data.drop(columns = ['event_timestamp', 'grade', 'interpol_type'])
        return self.new_df

    def data_stats(self):
        start = min(self.new_df.index)
        end = max(self.new_df.index)
        print('Start date:', start, '--- End date:', end)
        self.day_num = self.new_df.shape[0]
        print('Number of measurements:', self.day_num, '\n')

    def number_days(self):
        unique_date = len(self.new_df.index.unique())
        print('Number of unique days:', unique_date)

        delta = max(self.new_df.index)- min(self.new_df.index)
        print('Days between the first and the last measurement:',  delta.days)
        print('Days with no measurements:', (delta.days-self.day_num), '\n')

    def rain_days(self):
        rain_days = self.new_df['rain_value'].value_counts(dropna=True, sort=True)
        print('Days with no rain:', rain_days[0], '---', round(rain_days[0]/self.day_num *100, 0),'%')

        y = list(filter(lambda x: x <= 1, rain_days.index))
        little_rain = rain_days.values[0:14].sum()
        print('Days with rain, less than 1mm/day:', little_rain, '---', round(little_rain/self.day_num*100, 0), '%', '\n')

        df_sorted = self.new_df.sort_values(by = 'rain_value', ascending = False)
        print('Dates with the maximum rain falls:','\n')
        print(df_sorted.head(5))


def main():
   filename = '../Data/AucklandRainfall1872-1997.csv'
   print('Reading file ', filename, '...\n')

   rain_data = RainFall(filename)
   df = rain_data.read_input()
   print(df.head(5))

   print('Dropping unnecessary columns...')
   new_df = rain_data.clean_data()
   print(new_df.head(5), '\n')

   print('Basic statistics:')
   rain_data.data_stats()

   print('Number of days:')
   rain_data.number_days()

   print('Number of rain days:')
   rain_data.rain_days()

if __name__=="__main__":
    main()
