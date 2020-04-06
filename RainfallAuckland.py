#Time series analysis of rainfall data in Auckland between 1872 and 1997
import os
import numpy as np
import pandas as pd
from pandas import datetime
import matplotlib.pyplot as plt
import seaborn as snb
snb.set()

#Reading input file
def read_input(file):
   try:
      with open(file, 'r') as input_file:
         return (pd.read_csv(file,
                             skiprows=3,
                             header=None,
                             names=['timestamp','rain_value', 'grade', 'interpol_type', 'event_timestamp'],
                             parse_dates=['timestamp'],
                             index_col='timestamp'
                             ))
   except IOError:
      print("File not found or path is incorrect")

#Exploring stats of rainfall data
def rain_days_numbers(dataf):
    print('Basic statistics:', '\n')

    start=min(dataf.index)
    end=max(dataf.index)
    print('Start date:', start, '--- End date:', end)
    unique_date=len(dataf.index.unique())
    day_num=dataf.shape[0]
    print('Number of measurements:', day_num)
    print('Number of unique dates:', unique_date)

    delta=max(dataf.index)-min(dataf.index)
    print('Number of days between the first and last measurements:',  delta.days)
    print('Number of days with no measurements:', (delta.days-day_num), '\n')

    rain_days= dataf['rain_value'].value_counts(dropna=True, sort=True)
    print('Number of days with no rain:', rain_days[0], '---', round(rain_days[0]/day_num *100, 0),'%')

    y=list(filter(lambda x: x <= 1, rain_days.index))
    little_rain=rain_days.values[0:14].sum()
    print('Number of days with rain, less than 1mm/day:', little_rain, '---', round(little_rain/day_num*100, 0), '%', '\n')

    df_sorted=dataf.sort_values(by='rain_value', ascending=False)
    print('Dates with the maximum rain falls:', df_sorted.head(5))


def main():
   filename='Data/AucklandRainfall1872-1997.csv'
   print('Reading file ', filename, '...\n')
   df= read_input(filename)

   #exploring & cleaning data
   row_number=df.shape[0]
   print('Number of rows:', row_number)

   print('Dropping empty columns...')
   missing_number=df.event_timestamp.value_counts(dropna=False)
   #"'event_timestamp' column does not have values: missing_number == row_number)
   df=df.drop(columns=['event_timestamp', 'grade', 'interpol_type'])
   print(df.head(5), '\n')

   rain_days_numbers(df)

   print("Plotting data...")

   ax=plt.subplot(2,1,1)
   df['rain_value'].plot(kind='line', color='blue')
   plt.xlabel('Year')
   plt.ylabel('Rainfall (mm)')
   plt.title('Rainfall in Auckland')
   plt.grid(True)

   ax=plt.subplot(2,1,2)
   df_year=df.resample('Y').mean()
   df_year['rain_value'].plot(kind='line', color='green')
   df_year['rain_value'].rolling(2,center=True).mean().plot(style=['--'], color='red')
   plt.xlabel('Year')
   plt.ylabel('Rainfall (mm)')
   plt.title('Mean annual rainfall in Auckland')
   plt.grid(b=True, which='major', linestyle='-')
   plt.minorticks_on()
   plt.grid(b=True, which='minor', linestyle='-')
   plt.tight_layout()
   plt.show()

   plt.figure()
   ax=plt.subplot(2,1,1)
   df_new=df.groupby(df.index.month).median()
   months=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
   df_new.index=months
   df_new['rain_value'].plot(kind='line', color='blue', )
   plt.xlabel('Months')
   plt.ylabel('Rainfall (mm)')
   plt.title('Median monthly rainfall in Auckland between 1872 and 1997')
   plt.grid(b=True, which='major', linestyle='-')
   plt.minorticks_on()
   plt.grid(b=True, which='minor', linestyle='-')

   ax=plt.subplot(2,1,2)
   df_new2=df.groupby(df.index.week).median()
   df_new2['rain_value'].plot(kind='bar', color='green', grid='months')
   plt.xticks([ ])
   plt.xlabel('Jan      Feb      Mar    Apr    May   Jun   Jul   Aug    Sep    Oct      Nov    Dec')
   plt.ylabel('Rainfall (mm)')
   plt.title('Median weekly rainfall over period of 125 years')
   plt.grid(b=True, which='major', linestyle='-')
   plt.minorticks_on()
   plt.grid(b=True, which='minor', linestyle='-')
   plt.tight_layout()
   plt.show()


if __name__=="__main__":
    main()
