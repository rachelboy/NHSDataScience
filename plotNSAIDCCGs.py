import config
import util
import matplotlib.pyplot as pyplot
import numpy as np
import pandas
import thinkstats as ts
import thinkplot as tp

def makeIndChange(Config):
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
			inter_2, slope_2 = None,None
		x_1, y_1 = ts.FitLine(range(10), inter_1, slope_1)
		x_2, y_2 = ts.FitLine(range(10, 10+len(value[10:])), inter_2, slope_2)
		# pyplot.plot(x_1, y_1,label='fit pre-guidance')
		# pyplot.plot(x_2, y_2, label='fit post-guidance')
		# pyplot.plot(value, label = 'actual percent diclofenac')
		# pyplot.title('percent diclophenac over time for CCG '+key)
		# pyplot.xlabel('months since Jan 2012')
		# pyplot.ylabel('percent diclophenac')
		# pyplot.show()
		try:
			slope_diff = slope_2 - slope_1
		except TypeError:
			slope_diff = None
		# print slope_diff
		out['CCG'].append(key)
		try:
			out['Slope Diff (negated)'].append(-1*slope_diff)
		except TypeError:
			out['Slope Diff (negated)'].append(None)
		out['Slope 1'].append(slope_1)
		out['Inter 1'].append(inter_1)
		out['Slope 2'].append(slope_2)
		out['Inter 2'].append(inter_2)

		outDF = pandas.DataFrame(out)
		outDF.to_csv('Results/RateChange_NSAIDs.csv',index=False)

	
	# pyplot.plot(data['mean'], label = 'average')
	# pyplot.plot(data['dev_up'],'.', label = '1 std dev up')
	# pyplot.plot(data['dev_down'],'.', label = '1 std dev down')
	# pyplot.legend()
	# pyplot.title('Averge percent diclofenac over all CCGs (Jan 2012 to Oct 2013)')
	# pyplot.ylabel('Percent diclofenac')
	# pyplot.xlabel('Months since Jan 2012')
	# pyplot.show()

def plotLinearCDF(data,key,title,ylabel,xlabel):
	cdf = ts.MakeCdfFromList(data.to_dict(outtype='list')[key])
	scale = tp.Cdf(cdf, xscale='linear')
	tp.Config(title = title, 
		ylabel=ylabel, xlabel=xlabel, **scale)
	tp.Show()

def plotCCGDist(Config):
	data = pandas.read_csv('Results/RateChange_NSAIDs.csv')
	plotData = data[data['Inter 1'] >-1]
	plotLinearCDF(plotData,'Inter 1',
		'perc diclofenac in Jan 2012 by CCG group',
		'percent of CCG groups','percent diclofenac')

	plotLinearCDF(plotData,'Slope 1',
		'change per month of perc diclofenac before Apr 2012 by CCG group',
		'percent of CCG groups','percent diclofenac/month')

	plotData = data[data['Inter 2'] >-1]
	plotLinearCDF(plotData,'Slope 2',
		'change per month of perc diclofenac after Apr 2012 by CCG group',
		'percent of CCG groups','change in percent diclofenac per month')

	plotData['Oct2013'] = plotData['Inter 2'] + (plotData['Slope 2']*21)
	plotLinearCDF(plotData,'Oct2013',
		'perc diclofenac in Oct 2013 by CCG group',
		'percent of CCG groups','percent diclofenac')

def ClassifyCCGS(Config):
	data = pandas.read_csv('Results/RateChange_NSAIDs.csv')
	data['Tot_Before'] = data['Inter 1'].map(lambda x: 'missing data' if x!=x else ('high' if x > .45 else ('low' if x < .2 else 'med')))
	data['Slope_After'] = data['Slope 2'].map(lambda x: 'missing data' if x!=x else ('up' if x > 0 else ('down' if x <-.005 else 'neutral')))
	data.to_csv('Results/RateChange_NSAIDs.csv')

def reportClass(Config):
	data = pandas.read_csv('Results/RateChange_NSAIDs.csv')
	grouped = data.groupby(['Tot_Before','Slope_After'])
	# for name,group in grouped:
	# 	print name, len(group.index)

	column_labels = ['high','med','low']
	row_labels = ['up','neutral','down']
	data = []
	for c in column_labels:
		data.append([])
		for r in row_labels:
			try:
				data[-1].append(len(grouped.get_group((c,r)).index))
			except KeyError:
				data[-1].append(-8)
	data = np.array(data)
	fig, ax = pyplot.subplots()
	heatmap = ax.pcolor(data, cmap=pyplot.cm.Blues)

	# put the major ticks at the middle of each cell
	ax.set_xticks(np.arange(data.shape[0])+0.5, minor=False)
	ax.set_yticks(np.arange(data.shape[1])+0.5, minor=False)

	# want a more natural, table-like display
	ax.invert_yaxis()
	# ax.xaxis.tick_top()

	ax.set_xticklabels(row_labels, minor=False)
	ax.set_yticklabels(column_labels, minor=False)
	pyplot.title('Number of CCG groups in each category')
	pyplot.ylabel('Initial prescribing rate of diclofenac vs. naproxen')
	pyplot.xlabel('change in diclofenac prescribing rate after directive')
	pyplot.show()



if __name__ == "__main__":
	Config = config.Config()
	# makeIndChange(Config)
	# ClassifyCCGS(Config)
	reportClass(Config)

	