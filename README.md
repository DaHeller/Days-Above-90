# Climate Change: Analysis and Simple Model for days above 90 Degrees Fareinheight

## My Question:

Is it possible to predict how many days in a given year will be above 90 degrees? Using the features total precipitation, and the average atomsopheric CO2 content.





When meeting someone new a lot of the time you'll instinctively mention the weather,'Boy it sure is hot today!' or 'Dang it took my car fifteen minutes to warm up in this artic tundra we call Colorado.'. It makes sense for people to bring up the weather often as we are living inside of it but the weather always seems to be changing! 


## My Data and Methods:
NOAA CO2: 
ftp://aftp.cmdl.noaa.gov/products/trends/co2/co2_mm_mlo.txt

Division of Atmospheric Research, CSIRO CO2 Data: 
https://cdiac.ess-dive.lbl.gov/ftp/trends/co2/lawdome.combined.dat

NOAA Station Data:
ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/
NOAA Station Readme:
ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/readme.txt

After downloading the full station datasets I isolated all of the stations in Minnesota, then averaged the number of days above 90 and total precipitation for every year. Some of the stations go as far back as 1880 where-as others only go back as far as the early 1900's because of this I decided to choose my starting year as 1918 and my finishing year as 2018 giving us a century worth of data. 

As with most datasets there were some unrecorded values, the way I handled this was just by assuming that any day that the temperature was not recorded was below 90 degrees. I think this is a fair way of doing it as the missing values are spread among different seasons.

## Exploratory Data Analysis
PAIR PLOT PICTURE HERE

Lots of interesting plots here one of the most fascinating I see is the CO2/Year plot after 1950 it starts to grow exponentially. My theory is 1950 was a time of great growth for the transportation industrys, as-well as in the late 1960's Brazil started ramping up their deforestation efforts. In 1955 the first automobile companys sold over 6 million units in one year and by the end of the 50's commercial airlines were becoming more and more streamlined yet another contributer to the growth of CO2 in our atmosphere.

Another interesting plot is the Days Above 90 vs Year

ZOOMED IN PICTURE OF TMAX vs YEAR

HEATMAP PICTURE HERE
