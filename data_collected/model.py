######################################################################################################################################################################
#REQUIREMENTS for the model:
# Should be able to distinguish safe and unsafe behaviour given the requirements:
# - Look at the number of RSSI pings within ____ time - all data is for 1 min
# - Look at what the phone is placed in
# - Make a approx log graph for how fast covid is contracted - use to figure out the safe distance

######################################################################################################################################################################
#Import packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import os

os.chdir("combined_csv")

######################################################################################################################################################################
#Beginning configuration for the ML model
#In this model, you input where your phone was, and based on the id where the other person's phone was as well and it chooses one of the following linear regression models
######################################################################################################################################################################
#This is the function for the distance vs time for covid. 
def f(x): #This takes in x as the distance and outputs the time limit 
	return 15.9325 - (14.68626/2**(x/1.342586)) #For this, I plotted a few points: (0, 1), (1, 8), (2, 10), (11, 16) and fitted the curve using an online calculator

#Create Dataframes

model_list = ['none', 'one_purse', 'both_purse', 'one_hand', 'both_hand', 'one_cloth', 'both_cloth'] #This is mainly just for the function at the end and to remember the diff scenarios
#List of all csv files used
all_list = ["both_hand_list.csv", "trans_thin_list.csv", "rec_hand_list.csv", "rec_purse_list.csv", "none_list.csv", "trans_purse_list.csv", "both_purse_list.csv", "rec_thin_list.csv", "trans_hand_list.csv", "both_thin_list.csv"]

#Create function to read each csv file
def read_d(x):
	return pd.read_csv(x, header=0)

#Based on results from data_analysis.py, there is no sig diff between trans and rec data. This is why the two files are combined here.
none = read_d("none_list.csv")
one_purse = pd.concat([read_d("rec_purse_list.csv"), read_d("trans_purse_list.csv")])
both_purse = read_d("both_purse_list.csv")
one_hand = pd.concat([read_d("rec_hand_list.csv"), read_d("trans_hand_list.csv")])
both_hand = read_d("both_hand_list.csv")
one_cloth = pd.concat([read_d("rec_thin_list.csv"), read_d("trans_thin_list.csv")])
both_cloth = read_d("both_thin_list.csv")

#This calculates the total number of RSSI values in 1 min for each scenario (used in function at the end)
none_1min = none.shape[0]/11
one_purse_1min = one_purse.shape[0]/11
both_purse_1min = both_purse.shape[0]/11
one_hand_1min = one_hand.shape[0]/11
both_hand_1min = both_hand.shape[0]/11
one_cloth_1min = one_cloth.shape[0]/11
both_cloth_1min = both_cloth.shape[0]/11

#This is a list of all the times above, used by index in function at end
min_values_list = [none_1min, one_purse_1min, both_purse_1min, one_hand_1min, both_hand_1min, one_cloth_1min, both_cloth_1min]

######################################################################################################################################################################
#Separate data and create model
######################################################################################################################################################################

def split_d(data):
	#This function takes in a dataset and returns the X and y dataframes, where X has the RSSI values that are being inputted to predict the y, or distance.
	X = data["RSSI"].values.reshape(-1, 1)
	y = data["DISTANCE"].values.reshape(-1, 1)
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
	return X_train, X_test, y_train, y_test

#Split data for each scenario
X_train_none, X_test_none, y_train_none, y_test_none = split_d(none)
X_train_one_purse, X_test_one_purse, y_train_one_purse, y_test_one_purse = split_d(one_purse)
X_train_both_purse, X_test_both_purse, y_train_both_purse, y_test_both_purse = split_d(both_purse)
X_train_one_hand, X_test_one_hand, y_train_one_hand, y_test_one_hand = split_d(one_hand)
X_train_both_hand, X_test_both_hand, y_train_both_hand, y_test_both_hand = split_d(both_hand)
X_train_one_cloth, X_test_one_cloth, y_train_one_cloth, y_test_one_cloth = split_d(one_cloth)
X_train_both_cloth, X_test_both_cloth, y_train_both_cloth, y_test_both_cloth = split_d(both_cloth)

#Train the models on linear regressor.
regressor = LinearRegression()  

none_r = regressor.fit(X_train_none, y_train_none)
one_purse_r = regressor.fit(X_train_one_purse, y_train_one_purse)
both_purse_r = regressor.fit(X_train_both_purse, y_train_both_purse)
one_hand_r = regressor.fit(X_train_one_hand, y_train_one_hand)
both_hand_r = regressor.fit(X_train_both_hand, y_train_both_hand)
one_cloth_r = regressor.fit(X_train_one_cloth, y_train_one_cloth)
both_cloth_r = regressor.fit(X_train_both_cloth, y_train_both_cloth)

#List of all regression models
regressor_list = [none_r, one_purse_r, both_purse_r, one_hand_r, both_hand_r, one_cloth_r, both_cloth_r]

######################################################################################################################################################################
#Test the accurracy of the model
######################################################################################################################################################################

#Predict test data for each of the scenarios
y_pred_none = none_r.predict(X_test_none)
y_pred_one_purse = one_purse_r.predict(X_test_one_purse)
y_pred_both_purse = both_purse_r.predict(X_test_both_purse)
y_pred_one_hand = one_hand_r.predict(X_test_one_hand)
y_pred_both_hand = both_hand_r.predict(X_test_both_hand)
y_pred_one_cloth = one_cloth_r.predict(X_test_one_cloth)
y_pred_both_cloth = both_cloth_r.predict(X_test_both_cloth)

#Function to find error for each scenario
def fit_tester(x, a, b): #x is the category, a is the y test values and b is the predicted values for y
	print('\n')
	print(x)
	print('Mean Absolute Error:', metrics.mean_absolute_error(a, b))  
	print('Mean Squared Error:', metrics.mean_squared_error(a, b))  
	print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(a, b)))

fit_tester('none', y_test_none, y_pred_none) #MSE = 1.7929 RMSE = 1.3389
fit_tester('one_purse', y_test_one_purse, y_pred_one_purse) #MSE = 1.15758 RSME = 1.07591
fit_tester('both_purse', y_test_both_purse, y_pred_both_purse) #MSE = 1.3590 RSME = 1.16576
fit_tester('one_hand', y_test_one_hand, y_pred_one_hand) #MSE = 1.99763 RSME = 1.413377
fit_tester('both_hand', y_test_both_hand, y_pred_both_hand) #MSE = 7.633657 RSME = 2.76092
fit_tester('one_cloth', y_test_one_cloth, y_pred_one_cloth) #MSE = 0.64123 RSME = 0.80077
fit_tester('both_cloth', y_test_both_cloth, y_pred_both_cloth) #MSE = 0.860338 RSME = 0.927544


######################################################################################################################################################################
#Create algorithm that mimics a simplified version of the overall process 
######################################################################################################################################################################

def predict_distance(condition_phones, array_RSSI): 
	#This function takes in a string (condition_phones) that describes what condition the phones are in (what scenario) and an array with all the RSSI values
	tot_values = array_RSSI.shape[0] #Total values in the array
	ind = model_list.index(condition_phones) #Index of the scenario in the model_list at the beginning. This index is the same for the scenario in each list in this code
	min_contacted = tot_values / (min_values_list[ind]) #Total minutes that this specific situation went for 
	model = regressor_list[ind] #Calls the correct model from the regressor_list above
	pred = model.predict(array_RSSI) #Returns array with all predicted distances in meters(m)
	distance = np.mean(pred) #Takes the mean of the array to give a single distance
	safe_time = f(distance) #Calls the first function f on the distance above to find the time limit for the distance
	#The if/else returns whether the current time for the distance predicted is considered safe or not
	if min_contacted > safe_time: 
		print("Unsafe")
		return "Unsafe contact"
	else:
		print("Safe")
		return "Safe contact"

#Example:
predict_distance('none', np.array([[-40], [-42], [-47], [-50]]))





