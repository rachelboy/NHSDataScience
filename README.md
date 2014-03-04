NHSDataScience
==============

Modify config file to make code work on your system:
	self.data_directory should be the path to the directory containing all of the downloaded data files. 

Downloaded datafiles should be named "MonYear.csv", where Mon is the first three characters of the month, and Year is the four digit year. This is for both the data (in RawData) and the address files (in Addresses). To run the pipeline, all folders should be already created in self.data_directory.

You can use TestConfig, rather than Config, to test on a subset of files (parameters in TestConfig should be changed appropriately for your system). 

