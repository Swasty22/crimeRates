import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


#Reading CSV file
df = pd.read_csv('crimeData.csv')
#Dropping the unwanted column where axis=1 refers column
df = df.drop(["DR_NO","AREA","Rpt Dist No","Part 1-2","Mocodes"],axis=1)


#changing date format
df['Date Rptd'] = pd.to_datetime(df['Date Rptd'])
df['DATE OCC'] = pd.to_datetime(df['DATE OCC'])

#Extracting only dates
df['Date Rptd'] = df['Date Rptd'].dt.date
df['DATE OCC'] = df['DATE OCC'].dt.date

print(df.info())


