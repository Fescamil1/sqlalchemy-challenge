# sqlalchemy-challenge
SQLAlchemy Homework - Climate analysis on Honolulu, Hawaii. 

#### Climate Analysis and Exploration

Python and SQLAlchemy to do basic climate analysis and data exploration of the climate database. Analysis completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

##### Precipitation Analysis 

Design a query to retrieve the last 12 months of precipitation data and plot the results using a DataFrame `plot` method. 

![](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20210630001219136.png)

​	

#### Station Analysis

The number of stations available are: 9

```
The most active stations and their counts are shown below:
station: USC00519281 count= 2772
station: USC00519397 count= 2724
station: USC00513117 count= 2709
station: USC00519523 count= 2669
station: USC00516128 count= 2612
station: USC00514830 count= 2202
station: USC00511918 count= 1979
station: USC00517948 count= 1372
station: USC00518838 count= 511
```

```
Most active station ID: USC00519281
Lowest Temperature Recorded= 54.0
Highest Temperature Recorded= 85.0
Average Temperature Recorded= 71.66378066378067
```

Histogram of last 12 months of temperature observation data (TOBS) for station with most observations: 

![image-20210630232514351](C:\Users\franc\AppData\Roaming\Typora\typora-user-images\image-20210630232514351.png)
