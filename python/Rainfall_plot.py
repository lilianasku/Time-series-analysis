#Stats of time series Auckland rainfall data between 1872 and 1997
import sys
import numpy as np
import pandas as pd
import calendar
from datetime import datetime
import matplotlib.pyplot as plt

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
        if 'event_timestamp' and 'grade' and 'interpol_type' in self.input_data.columns:
           self.new_df = self.input_data.drop(columns = ['event_timestamp', 'grade', 'interpol_type'])
        else:
           self.new_df = self.input_data
        return self.new_df

    def mean_rainfall_plot(self, df):
        fig,ax = plt.subplots(2,1)
        ax[0].plot(df.index, df['rain_value'], color='blue')
        ax[0].set(xlabel = 'Year',
                ylabel = 'Rainfall (mm)',
                title = 'Rainfall in Auckland')

        df_monthly = df.resample('M').mean()
        df_year = df_monthly.rolling(12).mean()
        ax[1].plot(df_year.index, df_year['rain_value'], color='green')
        ax[1].set(xlabel ='Year',
             ylabel = 'Rainfall (mm)',
             title = 'Mean annual rainfall in Auckland')
        plt.tight_layout()
        plt.show()

    def median_rainfall_plot(self, df):
        fig,ax = plt.subplots(2,1)
        df_new2 = df.groupby(df.index.week).median()
        ax[0].bar(df_new2.index, df_new2['rain_value'], color='green')
        ax[0].set(xlabel = 'Weeks',
                  ylabel = 'Rainfall (mm)',
                  title = 'Median weekly rainfall in Auckland')

        df_new = df.groupby(df.index.month).median()
        months = [calendar.month_abbr[i] for i in range(1,13)]
        df_new.index = months
        ax[1].plot(df_new.index, df_new['rain_value'], color='blue', )
        ax[1].set(xlabel='Months',
               ylabel = 'Rainfall (mm)',
               title = 'Median monthly rainfall in Auckland between 1872 and 1997')
        plt.tight_layout()
        plt.show()

def main():
   filename='../Data/AucklandRainfall1872-1997.csv'
   print('Reading file ', filename, '...\n')

   rain_data = RainFall(filename)
   df = rain_data.read_input()
   try:
      print(df.head(5))
   except(AttributeError, NameError):
      print('Error with data frame:')
      sys.exit(1)

   print('Dropping unnecessary columns...')
   new_df = rain_data.clean_data()
   print(new_df.head(5), '\n')

   print("Plotting data...\n")
   rain_data.mean_rainfall_plot(new_df)
   rain_data.median_rainfall_plot(new_df)

if __name__=="__main__":
   main()
