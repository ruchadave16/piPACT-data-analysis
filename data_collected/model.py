######################################################################################################################################################################
#REQUIREMENTS for the model:
# Should be able to distinguish safe and unsafe behaviour given the requirements:
# - Look at the number of RSSI pings within ____ time - all data is for 1 min
# - Look at what the phone is placed in
# - Make a approx log graph for how fast covid is contracted - use to figure out the safe distance


# - Make second model with just considering distance
# - ML model that detects whether within 1m or not (3ft) - then it says unsafe immediately given what category it falls into

######################################################################################################################################################################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split 
from sklearn.linear_model import LinearRegression
from sklearn import metrics
import os

os.chdir("combined_csv")

######################################################################################################################################################################
#Model 1
######################################################################################################################################################################

def f(x): #This takes in x as the distance and outputs the time limit 
	return 18.49909 + ((0.9448442 - 18.49909)/(1 + (x/1.745409)^0.9872099)) #For this, I plotted a few points: (0, 1), (1, 8), (2, 10), (11, 16) and fitted the curve

#In this model, you input where your phone was, and based on the id where the other person's phone was as well and it chooses one of the following linear regression models
#Create Dataframes
model_list = ['none', 'one_purse', 'both_purse', 'one_hand', 'both_hand', 'one_cloth', 'both_cloth']

all_list = ["both_hand_list.csv", "trans_thin_list.csv", "rec_hand_list.csv", "rec_purse_list.csv", "none_list.csv", "trans_purse_list.csv", "both_purse_list.csv", "rec_thin_list.csv", "trans_hand_list.csv", "both_thin_list.csv"]

def read_d(x):
	return pd.read_csv(x, header=0)

none = read_d("none_list.csv")
one_purse = pd.concat([read_d("rec_purse_list.csv"), read_d("trans_purse_list.csv")])
both_purse = read_d("both_purse_list.csv")
one_hand = pd.concat([read_d("rec_hand_list.csv"), read_d("trans_hand_list.csv")])
both_hand = read_d("both_hand_list.csv")
one_cloth = pd.concat([read_d("rec_thin_list.csv"), read_d("trans_thin_list.csv")])
both_cloth = read_d("both_thin_list.csv")

#Split training and test data
def split_d(data):
	#This function takes in a dataset and returns the X and y dataframes, where X has the RSSI values that are being inputted to predict the y, or distance.
	X = data["RSSI"].values.reshape(-1, 1)
	y = data["DISTANCE"].values.reshape(-1, 1)
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
	return X_train, X_test, y_train, y_test

X_train_none, X_test_none, y_train_none, y_test_none = split_d(none)
X_train_one_purse, X_test_one_purse, y_train_one_purse, y_test_one_purse = split_d(one_purse)
X_train_both_purse, X_test_both_purse, y_train_both_purse, y_test_both_purse = split_d(both_purse)
X_train_one_hand, X_test_one_hand, y_train_one_hand, y_test_one_hand = split_d(one_hand)
X_train_both_hand, X_test_both_hand, y_train_both_hand, y_test_both_hand = split_d(both_hand)
X_train_one_cloth, X_test_one_cloth, y_train_one_cloth, y_test_one_cloth = split_d(one_cloth)
X_train_both_cloth, X_test_both_cloth, y_train_both_cloth, y_test_both_cloth = split_d(both_cloth)

#Train the models on simple regressor. Based on how the output is, see if a more complicated model is necessary
regressor = LinearRegression()  

none_r = regressor.fit(X_train_none, y_train_none)
one_purse_r = regressor.fit(X_train_one_purse, y_train_one_purse)
both_purse_r = regressor.fit(X_train_both_purse, y_train_both_purse)
one_hand_r = regressor.fit(X_train_one_hand, y_train_one_hand)
both_hand_r = regressor.fit(X_train_both_hand, y_train_both_hand)
one_cloth_r = regressor.fit(X_train_one_cloth, y_train_one_cloth)
both_cloth_r = regressor.fit(X_train_both_cloth, y_train_both_cloth)

#Test the models' accuracy
y_pred_none = none_r.predict(X_test_none)
y_pred_one_purse = one_purse_r.predict(X_test_one_purse)
y_pred_both_purse = both_purse_r.predict(X_test_both_purse)
y_pred_one_hand = one_hand_r.predict(X_test_one_hand)
y_pred_both_hand = both_hand_r.predict(X_test_both_hand)
y_pred_one_cloth = one_cloth_r.predict(X_test_one_cloth)
y_pred_both_cloth = both_cloth_r.predict(X_test_both_cloth)


def fit_tester(x, a, b):
	print('\n')
	print(x)
	print('Mean Absolute Error:', metrics.mean_absolute_error(a, b))  
	print('Mean Squared Error:', metrics.mean_squared_error(a, b))  
	print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(a, b)))

fit_tester('none', y_test_none, y_pred_none) #MSE = 1.7929 RMSE = 13389
fit_tester('one_purse', y_test_one_purse, y_pred_one_purse) #MSE = 1.15758 RSME = 1.07591
fit_tester('both_purse', y_test_both_purse, y_pred_both_purse) #MSE = 1.3590 RSME = 1.16576
fit_tester('one_hand', y_test_one_hand, y_pred_one_hand) #MSE = 1.99763 RSME = 1.413377
fit_tester('both_hand', y_test_both_hand, y_pred_both_hand) #MSE = 7.633657 RSME = 2.76092
fit_tester('one_cloth', y_test_one_cloth, y_pred_one_cloth) #MSE = 0.64123 RSME = 0.80077
fit_tester('both_cloth', y_test_both_cloth, y_pred_both_cloth) #MSE = 0.860338 RSME = 0.927544

#To compare this with other predicters: see if MSE can be lowered




