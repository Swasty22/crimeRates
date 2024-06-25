import folium.map
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium 
from folium.plugins import HeatMap

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

df['Date Rptd'] = pd.to_datetime(df['Date Rptd'])
df['DATE OCC'] = pd.to_datetime(df['Date Rptd'])

df['TIME OCC'] = df['TIME OCC'].astype(str)


#convert to Railway timing
from datetime import datetime

def convert_to_24hr_format(time_str):
    try:
        return datetime.strptime(time_str , '%H%M').strftime('%H:%M:%S')
    except ValueError:
        try:
            return datetime.strptime(time_str , '%I:%M %P').strftime('%H:%M:%S')
        except ValueError:
            return None

df['Hour'] = df['TIME OCC'].apply(convert_to_24hr_format)


#creating a new column Hour and extracting time from it 
df['Hour'] = pd.to_datetime(df['Hour'],format='%H:%M:%S').dt.time
#creating new column hout of day extracting only hour
df['Hour_of_day'] = pd.to_datetime(df['Hour'].astype(str),format='%H:%M:%S').dt.hour
#making copy of df and storing into df_copy
df_copy = df.copy()
df_copy = df_copy.dropna(subset=['Hour_of_day'])
#converting hour of day to int
df_copy['Hour_of_day'] = df_copy['Hour_of_day'].astype(int)

df=df_copy


#Getting day name from date occured
df['Day_Name'] = df['DATE OCC'].dt.day_name()

#No of crimes by each day
crime_in_days = df['Day_Name'].value_counts().reindex(
    ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']).fillna(0)



#Most crime is in:

colors = ['SkyBlue'] * len(crime_in_days)
monday_index = crime_in_days.index.get_loc('Monday')
colors[monday_index] = 'Red'
plt.figure(figsize=(10,6))
crime_in_days.plot(kind='bar',color=colors)
plt.title('Number of crimes per day')
plt.xlabel('Day')
plt.ylabel('No of crimes')
plt.xticks(rotation=0)
#plt.show()
#monday has most number of crimes

#crime count per hour

crime_in_hour = df['Hour_of_day'].value_counts().sort_index()
colors = ['SkyBlue']*len(crime_in_hour)
colors[9] = 'Red'
colors[12] = 'Red'
plt.figure(figsize=(10,6))
crime_in_hour.plot(kind='bar', color=colors)
plt.title('Number of crimes per hour')
plt.xlabel("Crime in hour")
plt.ylabel('No of crimes')
plt.xticks(rotation = 0)
#plt.show()
#maximum number of crime occurs between 11 am and 7 pm

#Analyze by season
df['season'] = df['DATE OCC'].dt.month.map({
    1:'Winter',2:'Winter',3:'Spring',4:'Spring',5:'Spring',6:'Summer',
    7:'Summer',8:'Summer',9:'Fall',10:'Fall',11:'Fall',12:'Winter'
})
crime_by_season = df.groupby('season').size()
labels = crime_by_season.index
size = crime_by_season.values
colors = ['SkyBlue','lightgreen','orange','red']
plt.pie(size , labels=labels , colors=colors , autopct= '%1.1f%%',
         startangle=140,wedgeprops={'edgecolor':'white','linewidth':2})
plt.axis('equal')
plt.title('Crime By Season')
#plt.show()
#print(f'Crime By season,{crime_by_season}')
#All season likely to be equal in crimes

#top 10 crime codes
n_crime_code = df['Crm Cd'].value_counts().sort_index()
top_10 = n_crime_code.nlargest(10)
plt.figure(figsize=(8,6))
top_10.plot(kind='bar',color = 'skyblue')
plt.title('Top 10 Crime Codes')
plt.xlabel('Crime Code')
plt.ylabel('Number of Crimes')
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
#plt.show()
#print(f'Top 10 crime codes {top_10}')

#top 10 crime desc
n_crime_desc = df.groupby('Crm Cd Desc').size()
large_10 = n_crime_desc.nlargest(10)
plt.figure(figsize=(8,6))
large_10.plot(kind='bar',color = 'skyblue')
plt.title('Top 10 crime Description')
plt.xlabel('Crime Description')
plt.ylabel('Number of Crimes')
plt.xticks(rotation = 90)
plt.grid(axis='y',linestyle='--',alpha=0.7)
#plt.show()
#print(f'Top 10 Crime description \n{large_10}')

#DISTRIBUTION OF CRIME BY SEX
crimes_in_gender =df['Vict Sex'].value_counts().sort_index()
plt.figure(figsize=(8,6))
sns.countplot(x='Vict Sex' , data=df , palette='pastel')
plt.title('Crimes By gender')
plt.xlabel('Gender')
plt.ylabel('Number of crimes')
#plt.show()
#print(f'Gender od Victim {crimes_in_gender}')

#Distribution of crime by age
plt.figure(figsize=(10,6))
plt.hist(df['Vict Age'] , bins=5,color='skyblue',edgecolor='black')
plt.title('Distribution of crime by age')
plt.xlabel('Age')
plt.ylabel("Number of crimes")
plt.grid(axis='y', linestyle='--', alpha=0.7)
#plt.show()

#top 10 weapon description
most_weapon = df['Weapon Desc'].value_counts().sort_index()
largest_10 = most_weapon.nlargest(10)
plt.figure(figsize=(8,6))
largest_10.plot(kind='bar',color='skyblue')
plt.title('Top 10 weapon description')
plt.xlabel('Weapons')
plt.ylabel('Number of occurences')
plt.xticks(rotation=45 , ha='right')
plt.grid(axis='y',linestyle='--',alpha=0.7)
plt.tight_layout()
#plt.show()
#print(f'top 10 Weapon occurences : {largest_10}')

crime_status = df['Status Desc'].value_counts().sort_index()
plt.figure(figsize=(8,6))
crime_status.plot(kind='barh',color='skyblue')
plt.title('Crime Status')
plt.xlabel('Number of crimes')
plt.ylabel('Status description')
plt.grid(axis='x', linestyle='--', alpha=0.7) 
plt.tight_layout()
#plt.show()
#print(f'Crime status :{crime_status}')

data = df[['LAT','LON']].dropna()
m = folium.Map(location=[data['LAT'].mean() , data['LON'].mean()],zoom_start=11)
heat_data = [[row['LAT'] , row['LON']] for index,row in data.iterrows()]
HeatMap(heat_data).add_to(m)
m.save('criminal_heatmap.html')
print(m)
