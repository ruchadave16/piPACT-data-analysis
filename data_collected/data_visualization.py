#Import needed modules
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd 
import numpy as np
import os

os.chdir("combined_csv")

######################################################################################################################################################################
#Edit files 
######################################################################################################################################################################

#Add scenario column to each file in the data folder that depicts what scenario is being included in the file
all_list = ["both_hand_list.csv", "trans_thin_list.csv", "rec_hand_list.csv", "rec_purse_list.csv", "none_list.csv", "trans_purse_list.csv", "both_purse_list.csv", "rec_thin_list.csv", "trans_hand_list.csv", "both_thin_list.csv"]
for x in all_list:
	data = pd.read_csv(x, header=0)
	data["SCENARIO"] = x[:-4]
	data.to_csv(x, index=False)

#Combine all files into one file that has all the data from all the experiments
combined_file = pd.concat([pd.read_csv(f) for f in all_list])
combined_file.to_csv("all_data.csv", index = False, encoding = 'utf-8-sig')

######################################################################################################################################################################
#Visualize
######################################################################################################################################################################

#Boxplot to see how each scenario varies
sns.boxplot(x="SCENARIO", y="RSSI", data=combined_file)
plt.clf()
#This shows that most of the datas look symmetrical, and there are a bunch of outliers in the data. The means for each value vary by a lot.
#The relative similarity between the plots doesn't matter because we didn't account for the distance differences in this plot 
	#So even if all of them have 40 and 50s, this doesn't matter because 40 could be at 1m for one scenario and at 3m for another

#Scatterplot color coded by scenario - all data:
sns.scatterplot(x="DISTANCE", y="RSSI", hue="SCENARIO", data=combined_file, palette='colorblind', legend='full')
plt.clf()



#Focus on the initial data, where there is no obstruction between the two raspberry pis to understand the basis of the experiment and the data collected.
#Read data
df = pd.read_csv('none_list.csv', header=0)
print(df.head(10))   

#Create scatterplot to see how each distance varies:
plt.scatter(df['DISTANCE'], df['RSSI'])
plt.clf()

#Add row to none_list - Based on scatterplot, it seems like 1m and > 1m have significant difference
#In this case, any distances less than 1m are in group A and more than 1 meter are in group B
df["GROUP"] = 'B'
for i in range(len(df)):
	if df["DISTANCE"][i] == 0.25 or df["DISTANCE"][i] == 0.5:
		df["GROUP"][i] = 'A'
print(df.head())

#Create distribution plot and color code by whether the distance is > 1m or < 1m
sns.FacetGrid(df, size=5, hue="GROUP").map(sns.distplot, "RSSI").add_legend()
plt.clf()
#This shows that the distributions for less than and greater than 1m are very different

#To create a similar distribution understanding of the complete dataset: to see if the 1m conclusion works for the whole dataset as well
comb_data = pd.read_csv('all_data.csv', header=0)
comb_data["GROUP"] = 'B'
for i in range(len(comb_data)):
    if comb_data["DISTANCE"][i] == 0.25 or comb_data["DISTANCE"][i] == 0.5:
        comb_data["GROUP"][i] = 'A'
print(df.head())

#Distribution plot for all data:
sns.FacetGrid(comb_data, size=5, hue="GROUP").map(sns.distplot, "RSSI").add_legend()
plt.clf()
#This shows that althought it is slightly more overlaping, the two distributions appear pretty different. 


