#Import needed modules
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd 
import os

os.chdir("combined_csv")

#Add scenario column to each file in the data folder
all_list = ["both_hand_list.csv", "trans_thin_list.csv", "rec_hand_list.csv", "rec_purse_list.csv", "none_list.csv", "trans_purse_list.csv", "both_purse_list.csv", "rec_thin_list.csv", "trans_hand_list.csv", "both_thin_list.csv"]
for x in all_list:
	data = pd.read_csv(x)
	data["SCENARIO"] = x[:-4]
	data.to_csv(x, index=False)

#Combine all files into one file of all data
combined_file = pd.concat([pd.read_csv(f) for f in all_list])
combined_file.to_csv("all_data.csv", index = False, encoding = 'utf-8-sig')





#Boxplot to see how each scenario varies
sns.boxplot(x="SCENARIO", y="RSSI", data=combined_file)
plt.show()
plt.clf()
#This shows that most of the datas look symmetrical, and there are a bunch of outliers in the data. The means for each value vary by a lot. The relative similarity doesn't matter because we didn't account for the distance in this plot

#Scatterplot with color coded - all data:
sns.scatterplot(x="DISTANCE", y="RSSI", hue="SCENARIO", data=combined_file, palette='colorblind', legend='full')
plt.show()
plt.clf()



#Focus on the initial data, where there is no obstruction between the two raspberry pis to understand the basis of my experiment and the data I've collected.
#Read data
df = pd.read_csv('none_list.csv')
df.head(10)   

#Create scatterplot to see how each distance varies:
plt.scatter(df['DISTANCE'], df['RSSI'])
plt.show()
plt.clf()

#Distribution for each distance



