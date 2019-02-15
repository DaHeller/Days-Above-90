import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random
import seaborn as sns
import statsmodels
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import RidgeCV

minesota_list=["USC00210018.dly", "USC00210075.dly", #list of stations to use in this case all minnesota stations
"USC00210252.dly",
"USC00210515.dly",
"USC00211465.dly",
"USC00211630.dly",
"USC00212142.dly",
"USC00212645.dly",
"USC00212698.dly",
"USC00212737.dly",
"USC00212916.dly",
"USC00213290.dly",
"USC00213303.dly",
"USC00214106.dly",
"USC00214652.dly",
"USC00215175.dly",
"USC00215400.dly",
"USC00215563.dly",
"USC00215615.dly",
"USC00215638.dly",
"USC00215887.dly",
"USC00216152.dly",
"USC00216547.dly",
"USC00216565.dly",
"USC00217087.dly",
"USC00217405.dly",
"USC00217460.dly",
"USC00218419.dly",
"USC00218618.dly",
"USC00219046.dly",
"USC00219249.dly",
"USW00014922.dly",
"USW00094967.dly"]

station_tmax_dict = {}
station_prcp_dict = {}
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)

for stationfilename in minesota_list:#for loop to go through all the file names
    key_tmax = stationfilename + "TMAX" #way of creating variable keys for the dictionary 
    key_prcp = stationfilename + "PRCP"
    tmax_arr = [] #list of lists every list inside is a row
    prcp_arr = [] 
    station = open("/home/david/galvanize/capstones/weatherdata/ghcnd_hcn/{}".format(stationfilename),"r") #open the file based on where it is in father loop
    for line in station: #loop to read every line and append the actual data
        if line[17:21] == "TMAX" or line[17:21] == "PRCP":
            vals=[]
            instancer = 0
            ID = line[0:11]
            year = line[11:15]
            month = line[15:17]
            element = line[17:21]
            vals=[ID,int(year),int(month),element]
            for num in range(0,31):
                if line[22+instancer:26+instancer] != "9999":
                    if line[17:21] == "TMAX":
                        z = ((float(line[22+instancer:26+instancer])/10) * (9/5) +32) #add the data to the list of lists
                        vals.append(round(z,1)) #also convert to farenheight
                        instancer+=8
                    if line[17:21] == "PRCP": #dont convert PRCP values to farenheight
                        vals.append(float(line[22+instancer:26+instancer])/10)
                        instancer+=8
                else:
                    vals.append(float(line[22+instancer:26+instancer])) #if it is 9999 just append 9999
                    instancer+=8
        if line[17:21] == "TMAX": #choose which dictonary to actual append results to
            tmax_arr.append(vals)
        if line[17:21] == "PRCP":
            prcp_arr.append(vals)
    value_tmax = pd.DataFrame(tmax_arr) #convert them to dataframes before makingit value in dictionary
    value_prcp = pd.DataFrame(prcp_arr)
    station_tmax_dict[key_tmax] = value_tmax #turn the key and value into an actual dictionary entry
    station_prcp_dict[key_prcp] = value_prcp

true_df_dict = {}
df_comp = []
counter = 0
for keytmax, keyprcp in zip(list(station_tmax_dict.keys()), list(station_prcp_dict.keys())): #for every actual DF in the dict
    df_tmax = station_tmax_dict[keytmax]
    df_prcp = station_prcp_dict[keyprcp]
    row1_arr = []
    actual_id = minesota_list[counter]
    for yearnum in range(1918, df_tmax[1].max()): #hardcode 1918 instead of df_tmax[1].min()
        tmax_temp_df = df_tmax[df_tmax[1]==yearnum] #cycle through year 1918->present in every indivudal df
        prcp_temp_df = df_prcp[df_prcp[1]==yearnum]
        if len(tmax_temp_df)==12: #only take values if there is data for every month of the year
            row1_arr_df = [actual_id,yearnum] #first data points in a row, the row temp list
            
            tmax_row=tmax_temp_df.iloc[:,4:] #take the data points for the days not for stationid, ele, etc...
            prcp_row=prcp_temp_df.iloc[:,4:]
            truefalse_tmax = (tmax_row>=90) & (tmax_row<1000) #count the days that are above 90
            truefalse_prcp = (prcp_row>0) & (prcp_row<9999) #record the prcp if its above 0
            
            year_total_days90 = np.sum(np.sum(truefalse_tmax)) #sum how many days are above 90
            year_total_prcp= np.sum(np.sum(prcp_row[truefalse_prcp])) #sum the percep column 
            
            row1_arr_df.append(year_total_days90) #append this to the temp list that stands for each row
            row1_arr_df.append(year_total_prcp)
            
            row1_arr.append(row1_arr_df) #append this to the list of lists for the df
            df_comp.append(row1_arr_df) #major df area where all the station values are kept
            
    true_df_dict[actual_id] = pd.DataFrame(row1_arr) #create a dictionary incase I want to come back later and get more granular
    counter +=1



df3 = pd.DataFrame(df_comp) #make a df that has all the info at every year
df3 = df3.sort_values(1) # sort by the year
df3 = df3.reset_index()# reset the index because the sort has messed up the index
df3.drop('index',axis=1,inplace=True) #drop the index column as reseting the index has moved the old index into a new col
df3.columns= ["station_id","year","daysabove90","total_precip"] #rename the columns
df3.drop('station_id',axis=1,inplace=True) #drop the station ids as they are irrelevant now



df2 = round(df3.groupby(['year']).mean()) #new dataframe that averages all the values that have equal years
df2.reset_index(inplace=True) #reset the index again as the group by has messed it up again




co2 = open("co2data.txt","r") #Custom text file with just the year and avgCO2 amount from CSIRO
co2df = []
for line in co2: #read the non-noaa co2data and append to a list
    yearco2 = int(line[0:4])
    co2val= float(line[21:26])
    co2df.append([yearco2,co2val]) #append to a list of lists that will become a Dataframe
co2noaa = open("co2noaadata.txt","r") #Custom text file with the date and all the associated values from NOAA CO2
co2dfnoaa=[]
for line in co2noaa: #read the noaa co2data and append to a list
    yearco2 = int(line[0:4])
    co2val= float(line[26:32])
    co2dfnoaa.append([yearco2,co2val]) #append to a list of lists that will become a Dataframe
co2df= pd.DataFrame(co2df)# convert both lists to a dataframe
co2dfnoaa=pd.DataFrame(co2dfnoaa)
co2dfnoaa = round(co2dfnoaa.groupby([0]).mean(),2) #since noaa data went monthly group by the year then take the average value

co2dfnoaa.reset_index(inplace=True) #reset the group-by index 
co2dfnoaa.columns=['year','avgco2'] #rename the columns
co2df.columns=['year','avgco2']
frames = [co2df, co2dfnoaa] #put both dataframes into a listfor the concat function

maindf = pd.concat(frames) #create a df that is a full list from 1918 to 2018 of avg co2 values for each year
maindf.reset_index(inplace=True)#reset index
maindf.drop('index',axis=1,inplace=True)#drop new index col
df = df2.merge(maindf, on='year') #merge the co2 data with the precip and tmax days we now have our working df
df.replace(df['avgco2'][66], 344.45,inplace=True) #replace 1984 with the average of 11 months as one measurment was missing