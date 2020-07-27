# piPACT-data-analysis
MIT piPACT individual project

The data collected folder contains all the data and code.

Individual files are all 109 of the initial csv files from the Raspberry pi. 
Combined files contain the files that were created by combining all the files from one scenario together, along with combining all the rec and trans files together.
The all_data file contains all data collected over the project

combine_files.py has most of the code to create these combined files along with a list of exactly which file contains what data. 

data_visualization.py has code to create the graphs and plots - visualize the data

data_analysis.py creates the trans and rec files, assesses normality for the two groups, and performs a paired t-test to see whether differences between the two are significant or not.

model.py creates a linear regression model for each scenario and uses an algorithm to conclude whether the situation is safe or unsafe.
