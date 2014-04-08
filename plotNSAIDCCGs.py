import config
import util
import matplotlib.pyplot as pyplot
import numpy as np
import pandas
import thinkstats as ts
import thinkplot as tp

if __name__ == "__main__":
	Config = config.Config()

	infiles = Config.append_dir('NSAIDCCG')
	data = {}
	out = {}
	out['CCG'] = []
	out['Slope Diff (negated)'] = []
	out['Slope 1'] = []
	out['Inter 1'] = []
	out['Slope 2'] = []
	out['Inter 2'] = []

	# data['mean'] = []
	# data['dev_up'] = []
	# data['dev_down'] = []
	for infile in infiles:
		mon = pandas.read_csv(infile)
		# mean = np.mean(mon['percent'])
		# std_dev = np.std(mon['percent'])
		# data['mean'] = [mean] + data['mean']
		# data['dev_up'] = [mean+std_dev] + data['dev_up']
		# data['dev_down'] = [mean-std_dev] + data['dev_down']

		
		for index,row in mon.iterrows():
			data[row['CCG']] = [row['percent']] + data.get(row['CCG'],[]) 
	for key, value in data.items():
		inter_1, slope_1 = ts.LeastSquares(range(10),value[0:10])
		try:
			inter_2, slope_2 = ts.LeastSquares(range(10, 10+len(value[10:])),value[10:])
		except ZeroDivisionError:
			print key + ' does not have enough data'
		x_1, y_1 = ts.FitLine(range(10), inter_1, slope_1)
		x_2, y_2 = ts.FitLine(range(10, 10+len(value[10:])), inter_2, slope_2)
		pyplot.plot(x_1, y_1,label='fit pre-guidance')
		pyplot.plot(x_2, y_2, label='fit post-guidance')
		pyplot.plot(value, label = 'actual percent diclofenac')
		pyplot.title('percent diclophenac over time for CCG '+key)
		pyplot.xlabel('months since Jan 2012')
		pyplot.ylabel('percent diclophenac')
		pyplot.show()
		# slope_diff = slope_2 - slope_1
		# print slope_diff
		# out['CCG'].append(key)
		# out['Slope Diff (negated)'].append(-1*slope_diff)
		# out['Slope 1'].append(slope_1)
		# out['Inter 1'].append(inter_1)
		# out['Slope 2'].append(slope_2)
		# out['Inter 2'].append(inter_2)

		# outDF = pandas.DataFrame(out)
		# outDF.to_csv('Results/RateChange_NSAIDs.csv',index=False)

	
	# pyplot.plot(data['mean'], label = 'average')
	# pyplot.plot(data['dev_up'],'.', label = '1 std dev up')
	# pyplot.plot(data['dev_down'],'.', label = '1 std dev down')
	# pyplot.legend()
	# pyplot.title('Averge percent diclofenac over all CCGs (Jan 2012 to Oct 2013)')
	# pyplot.ylabel('Percent diclofenac')
	# pyplot.xlabel('Months since Jan 2012')
	# pyplot.show()