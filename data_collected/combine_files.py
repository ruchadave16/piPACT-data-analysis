#Import all modules needed to create files
import os 
import glob
import pandas as pd 

#Move to right path
os.chdir("individual_data_csv")

#List all CSV Files in directory
rootdir = 'C:/Users/kinnari/Documents/GitHub/piPACT-data-analysis/data_collected/individual_data_csv/**/*'

none_list = glob.glob('none*.csv')
rec_thin_list = glob.glob('rec_thin*.csv')
trans_thin_list = glob.glob('trans_thin*.csv')
both_thin_list = glob.glob('both_thin*.csv')
rec_purse_list = glob.glob('rec_purse*.csv')
trans_purse_list = glob.glob('trans_purse*.csv')
both_purse_list = glob.glob('both_purse*.csv')
rec_hand_list = glob.glob('rec_hand*.csv')
trans_hand_list = glob.glob('trans_hand*.csv')
both_hand_list = glob.glob('both_hand*.csv')

all_scenarios = [none_list, rec_thin_list, trans_thin_list, both_thin_list, rec_purse_list, trans_purse_list, both_purse_list, rec_hand_list, trans_hand_list, both_hand_list]
all_scenarios_names = ["none_list", "rec_thin_list", "trans_thin_list", "both_thin_list", "rec_purse_list", "trans_purse_list", "both_purse_list", "rec_hand_list", "trans_hand_list", "both_hand_list"]

#Concatenate files that belong to one scenario:
def createOneCSV(file_list, output_file):
	result = pd.concat([pd.read_csv(file) for file in file_list])
	result.to_csv(output_file, index=False, encoding="utf-8")

for i in range(len(all_scenarios_names)):
	output_file = all_scenarios_names[i] + ".csv"
	createOneCSV(all_scenarios[i], output_file)