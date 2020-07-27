#Import
import pandas as pd
import os
from scipy import stats
import numpy as np
from scipy.stats import shapiro

os.chdir("combined_csv")

#Create files needed - combine the trans files into one file and the rec files into one file
trans_rec = ["trans_thin_list.csv", "rec_hand_list.csv", "rec_purse_list.csv", "trans_purse_list.csv", "rec_thin_list.csv", "trans_hand_list.csv"]
trans_list = []
trans_list.append(trans_rec[0])
trans_list.append(trans_rec[3])
trans_list.append(trans_rec[5])
rec_list = []
rec_list.append(trans_rec[1])
rec_list.append(trans_rec[2])
rec_list.append(trans_rec[4])

combined_file_t = pd.concat([pd.read_csv(f) for f in trans_list])
combined_file_r = pd.concat([pd.read_csv(f) for f in rec_list])

combined_file_t.to_csv("trans_all_list.csv", index = False, encoding = 'utf-8-sig')
combined_file_r.to_csv("rec_all_list.csv", index = False, encoding = 'utf-8-sig')


###################################################################################################################################################################
#Check if significant diff between trans and rec data
#Perform two sample t test

#Null: The RSSI values for the trans and rec list with the same other variables are the same
#Alternate: The RSSI values for the trans and rec list are different
#90% confidence level
###################################################################################################################################################################

df = pd.read_csv('trans_all_list.csv')
df_rec = pd.read_csv('rec_all_list.csv')

#Create table with Distance and RSSI - finds the mean of the RSSI values for each distance.
trans_table = df.groupby(["DISTANCE"])["RSSI"].mean()
rec_table = df_rec.groupby(["DISTANCE"])["RSSI"].mean()
print(trans_table)
print(rec_table)

#Normality test
stat, p = shapiro(df["RSSI"])
stat_r, p_r = shapiro(df_rec["RSSI"])

print("Trans is: ", stat, p, " and rec is: ", stat_r, p_r)

#The values of the normality test are: 0.947 for trans and 0.939 for rec --> this means both are approximately normally distributed, and a t test can be performed on the data
#Now run a paired t-test: for each distance, you want the two means to be compared

print(stats.ttest_rel(trans_table, rec_table))

#This results in the test statistic being 1.97032 and the p-value being 0.07710
#Because the alpha value selected is 0.10, the current p-value is lower than this, meaning that the alternate can be rejected. 
#There is no significant difference between the trans and rec data --> which pi is being affected does not change the data significantly for this experiment.




