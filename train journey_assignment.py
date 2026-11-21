#!/usr/bin/env python
# coding: utf-8

# ### EXAM ASSIGNMENT
# NAME: OKOTH GEORGE ODHIAMBO
# REG. NO: 202608405
# UNIT:The Fourth industrial revolution and Application of software (001)
# PROF: Lic Ren Tai
# 
# Topic: **A simple research using railway train journeys dataset**
# 
# Company dataset: train_journeys.csv
# 
# REQUIREMENT:
# Imagine you obtain some data and records on train journeys provided by your company. You want to examine the data and investigate on journey performance so that you can suggest improvements on the services provided by your company. 
# 
# Annalysis research Questions:
# 
# 1. a)Which routes have the highest average passenger numbers?
#    b) Route with the highest average passenger limit
#    c) Route with the lowest average passenger limit
#    d)Plot a graph showing Top 5 Routes by Average Passenger Numbers. 
# 
# 2.  a)Which destinations attract the highest number of passengers?
#     b) Destination attracting the highest number of passengers 
#     c) Destination attracting the lowest number of passengers
#     C)Plot the top 5 destinations.
# 
# 3. (a)Establish if there a relationship between ticket price and   passenger numbers?
#    (b)Inteprete the existing correlation
#    (c)Plot a scatter graph indicating the existing correlation.
#    (d)Add a trend line showing the correlation results.
# 
# 4.  (a)What is the distribution of delay severity across all journeys?
#     (b)Plot the distribution of Delay Severity Across the  Train Journeys
#     (c)Plot the percentage distribution of Delay Severity across the train journey.
#     

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# In[6]:


# Q5. Which routes have the highest average passenger numbers?

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("DATA/train_journeys.csv")

#print(df.head())
#print(df.info())

# Create route
df["route"] = df["station"] + " - " + df["destination"]

# Analyse average passengers by route
route_passengers = (
    df.groupby("route")
      .agg(
          TOTAL_TRIPS=("journey_id", "count"),
          AVG_PASSENGERS=("passengers", "mean"),
          MAX_PASSENGERS=("passengers", "max"),
          TOTAL_PASSENGERS=("passengers", "sum")
      )
      .sort_values("AVG_PASSENGERS", ascending=False)
      .round(1)
)

print(route_passengers)


# In[7]:


# Q1(b)Print the route with the highest average passenger numbers

highest_route = route_passengers["AVG_PASSENGERS"].idxmax()
highest_average = route_passengers["AVG_PASSENGERS"].max()

print("Route with the highest average passenger numbers:", highest_route)
print("Average passengers:", highest_average)


# In[11]:


print("Highest passenger route:")
print(route_passengers.iloc[0])


# In[8]:


# Q1(c)Print the route with the lowest average passenger numbers

lowest_route = route_passengers["AVG_PASSENGERS"].idxmin()
lowest_average = route_passengers["AVG_PASSENGERS"].min()

print("Route with the lowest average passenger numbers:", lowest_route)
print("Average passengers:", lowest_average)


# In[12]:


print("Lowest passenger route:")
print(route_passengers.iloc[-1])


# In[13]:


route_passengers["AVG_PASSENGERS"].head(5).plot(
    kind="bar",
    figsize=(10, 5)
)

plt.title("Top 5 Routes by Average Passenger Numbers")
plt.xlabel("Train Route")
plt.ylabel("Average Passengers")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# In[20]:


 #Q(2)(a)Which destinations attract the highest number of passengers?
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("DATA/train_journeys.csv")

#print(df.head())
#print(df.info())

destination_passengers = (
    df.groupby("destination")
      .agg(
          TOTAL_TRIPS=("journey_id", "count"),
          TOTAL_PASSENGERS=("passengers", "sum"),
          AVG_PASSENGERS=("passengers", "mean"),
          MAX_PASSENGERS=("passengers", "max")
      )
      .sort_values("TOTAL_PASSENGERS", ascending=False)
      .round(1)
)

print(destination_passengers)


# In[ ]:


highest_destination = destination_passengers["TOTAL_PASSENGERS"].idxmax()

highest_passengers = destination_passengers["TOTAL_PASSENGERS"].max()

print("Destination attracting the highest number of passengers:", highest_destination)
print("Total passengers:", highest_passengers)


# In[21]:


# Q2(b)Print the destination attracting the lowest number of passengers

lowest_destination = destination_passengers["TOTAL_PASSENGERS"].idxmin()

lowest_passengers = destination_passengers["TOTAL_PASSENGERS"].min()

print("Destination attracting the lowest number of passengers:", lowest_destination)
print("Total passengers:", lowest_passengers)


# In[19]:


#c) Plot the top 5  destinations.
destination_passengers["TOTAL_PASSENGERS"].head(5).plot(
    kind="bar",
    figsize=(10, 5)
)

plt.title("Top 5 Destinations by Total Passenger Numbers")
plt.xlabel("Destination")
plt.ylabel("Total Passengers")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# In[ ]:


# Q3 Calcute realationship
# Q3(a). Relationship between ticket price and passenger numbers

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("DATA/train_journeys.csv")

# Calculate correlation
correlation = df["ticket_price"].corr(df["passengers"])

print("Correlation between ticket price and passenger numbers:", round(correlation, 3))


# In[ ]:


# Q3(b)Correlation value	Interpretation
#Close to +1	Strong positive relationship
#Close to -1	Strong negative relationship
#Close to 0	Weak or no linear relationship

 #The relationship between ticket price and passenger numbers is almost zero.


# In[25]:


#Q3(c)Scatter Graph plot
plt.figure(figsize=(9, 5))

plt.scatter(df["ticket_price"], df["passengers"])

plt.title("Relationship Between Ticket Price and Passenger Numbers")
plt.xlabel("Ticket Price")
plt.ylabel("Number of Passengers")

plt.grid(True)
plt.show()


# In[26]:


#Q3(d)  Trend line plot
x = df["ticket_price"]
y = df["passengers"]

plt.figure(figsize=(9, 5))

plt.scatter(x, y)

m, b = np.polyfit(x, y, 1)

plt.plot(x, m*x + b)

plt.title("Ticket Price vs Passenger Numbers with Trend Line")
plt.xlabel("Ticket Price")
plt.ylabel("Number of Passengers")

plt.show()


# In[ ]:


# Q4.(a)  What is the distribution of delay severity across all journeys?
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("DATA/train_journeys.csv")

#print(df.head())
#print(df.info())

# Categorise delay severity
df["DELAY_CATEGORY"] = pd.cut(
    df["delay_minutes"],
    bins=[-1, 5, 15, 30, float("inf")],
    labels=["On time/Minimal", "Minor", "Moderate", "Severe"]
)

# Analyse delay distribution
delay_distribution = (
    df.groupby("DELAY_CATEGORY", observed=False)
      .agg(
          TOTAL_JOURNEYS=("journey_id", "count"),
          AVG_DELAY=("delay_minutes", "mean")
      )
)

# Calculate percentage of journeys
delay_distribution["PERCENTAGE"] = (
    delay_distribution["TOTAL_JOURNEYS"] / len(df) * 100
)

delay_distribution = delay_distribution.round(1)

print(delay_distribution)


# In[ ]:


# Delay categories used
# Category	Delay minutes
# On time/Minimal	0–5
# Minor	            6–15
# Moderate	        16–30
# Severe	        Above 30


# In[ ]:


# Q4(b) Plot of  the delay severity distribution
delay_distribution["TOTAL_JOURNEYS"].plot(
    kind="bar",
    figsize=(9, 5)
)
plt.title("Distribution of Delay Severity Across Train Journeys")
plt.xlabel("Delay Category")
plt.ylabel("Number of Journeys")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# In[34]:


# Q4(c)Percentage Distribution of Delay Severity
delay_distribution["PERCENTAGE"].plot(
    kind="bar",
    figsize=(9, 5)
)
plt.title("Percentage Distribution of Delay Severity")
plt.xlabel("Delay Category")
plt.ylabel("Percentage of Journeys (%)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# **RESEARCH CONCLUSION & INTERPRETATION**
# 
# Q1:-Route with the highest average passenger numbers: Daegu - Gwangju.average passengers: 309.0
#       -Route with the lowest average passenger numbers: Daegu - Incheon
# Average passengers: 86.0
# The routes with the highest average passenger numbers represent routes with stronger passenger demand per journey. Railway management could consider increasing capacity, using larger trains, or increasing service frequency on these routes.
# 
# Q2:-Destination attracting the highest number of passengers: Daejeon
# Total passengers: 1646.
# -Destination attracting the lowest number of passengers: Seoul-Total passengers: 587 .
# -Destinations with the highest total passenger numbers represent the strongest passenger traffic in the  dataset. This information can assist railway management in planning station capacity, passenger facilities, service frequency and resource allocation.
# 
# Q3:A correlation coefficient of -0.067 indicates a very weak negative linear relationship between ticket prices and passenger numbers.
# This means:
# - As ticket prices increase, passenger numbers show a very slight tendency to decrease.
# - However, the relationship is extremely weak.
# - Ticket price alone does not appear to have a meaningful linear association with passenger numbers in this dataset.
# The analysis established a Pearson correlation coefficient of -0.067 between ticket prices and passenger numbers. This indicates a negligible negative relationship between the two variables. The finding suggests that variations in ticket prices are not strongly associated with changes in passenger demand within the sampled train journeys.The railway company should not rely on ticket price adjustments alone to influence passenger demand. Other factors, including route popularity, service frequency, journey duration, convenience and service reliability, should also be investigated.
# 
# Q4.Key observations
# - 76.7% of journeys (23 out of 30) experienced on-time or minimal delays of 5 minutes or less.
# - 16.7% of journeys (5) experienced minor delays of between 6 and 15 minutes.
# - 6.7% of journeys (2) experienced moderate delays of between 16 and 30 minutes.
# - No journeys experienced severe delays exceeding 30 minutes.
# - Overall, 23.3% of journeys experienced delays exceeding 5 minutes.
# 
# -The analysis of 30 train journeys revealed that 76.7% (23 journeys) experienced on-time or minimal delays of 5 minutes or less, with an average delay of 2.2 minutes within this category. Minor delays accounted for 16.7% (5 journeys), averaging 9 minutes, while moderate delays represented 6.7% (2 journeys), with an average delay of 19.5 minutes. No severe delays exceeding 30 minutes were recorded. Overall, the findings indicate that railway operations demonstrated relatively good punctuality within the sampled journeys, although 23.3% experienced delays exceeding 5 minutes. Management should investigate the causes of minor and moderate delays to improve service reliability and operational efficiency.
# -The railway company should maintain its existing operational practices that support punctuality while investigating the causes of journeys experiencing delays above 5 minutes. Particular attention should be given to the two journeys with moderate delays to determine whether these resulted from infrastructure problems, operational inefficiencies, train faults or other disruptions.
# 
#  
# 
# **CLOSING REMARK:**
# 
# -With only 30 journey records, this result should be treated as preliminary. It does not establish that ticket prices have no effect on passenger demand, nor does it demonstrate causation.
# 
# -The results reveals that most train journeys experience minimal delays or whether moderate and severe delays are common. This can help railway management prioritise operational improvements according to the severity and frequency of delays.
# 
# -The analysis established a Pearson correlation coefficient of -0.067 between ticket prices and passenger numbers. This indicates a negligible negative relationship between the two variables. The finding suggests that variations in ticket prices are not strongly associated with changes in passenger demand within the sampled train journeys.
# 
# -Destinations with the highest total passenger numbers represent the strongest passenger traffic in your dataset. This information can assist railway management in planning station capacity, passenger facilities, service frequency and resource allocation.
# 
# -The routes with the highest average passenger numbers represent routes with stronger passenger demand per journey. Railway management could consider increasing capacity, using larger trains, or increasing service frequency on these routes.
# ___
# **END**
