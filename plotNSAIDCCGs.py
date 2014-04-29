import config
import util
import matplotlib.pyplot as pyplot
import numpy as np
import pandas
import thinkstats as ts
import thinkplot as tp
import math

def makeIndChangePCT(Config):
	infiles = Config.append_dir('NSAIDGov')
	data = {}
	out = {}
	out['PCT'] = []
	out['Oct2012'] = []
	out['Apr2013'] = []
	out['Slope Diff (negated)'] = []
	out['Slope 1'] = []
	out['Inter 1'] = []
	out['Slope 2'] = []
	out['Inter 2'] = []

	# data['mean'] = []
	# data['dev_up'] = []
	# data['dev_down'] = []
	for infile in infiles[7:]:
		mon = pandas.read_csv(infile)
		# mean = np.mean(mon['percent'])
		# std_dev = np.std(mon['percent'])
		# data['mean'] = [mean] + data['mean']
		# data['dev_up'] = [mean+std_dev] + data['dev_up']
		# data['dev_down'] = [mean-std_dev] + data['dev_down']

		
		for index,row in mon.iterrows():
			data[row['PCT']] = [row['percent']] + data.get(row['PCT'],[]) 
	for key, value in data.items():
		out['PCT'].append(key)
		if len(value) == 15:
			inter_1, slope_1 = ts.LeastSquares(range(10),value[0:10])
			inter_2, slope_2 = ts.LeastSquares(range(9, 15),value[9:15])
			x_1, y_1 = ts.FitLine(range(10), inter_1, slope_1)
			x_2, y_2 = ts.FitLine(range(9, 15), inter_2, slope_2)
			# pyplot.plot(x_1, y_1,label='fit pre-guidance')
			# pyplot.plot(x_2, y_2, label='fit post-guidance')
			# pyplot.plot(value, label = 'actual percent diclofenac')
			# pyplot.title('percent diclophenac over time for CCG '+key)
			# pyplot.xlabel('months since Jan 2012')
			# pyplot.ylabel('percent diclophenac')
			# pyplot.show()
			slope_diff = slope_2 - slope_1

			out['Oct2012'].append(value[9])
			out['Apr2013'].append(value[14])
			out['Slope 1'].append(slope_1)
			out['Inter 1'].append(inter_1)
			out['Slope 2'].append(slope_2)
			out['Inter 2'].append(inter_2)
			out['Slope Diff (negated)'].append(-1*slope_diff)
		else:
			out['Oct2012'].append(None)
			out['Apr2013'].append(None)
			out['Slope Diff (negated)'].append(None)
			out['Slope 1'].append(None)
			out['Inter 1'].append(None)
			out['Slope 2'].append(None)
			out['Inter 2'].append(None)

		outDF = pandas.DataFrame(out)
		outDF.to_csv('Results/RateChange_NSAIDs.csv',index=False)

def makeIndChange(Config):
	infiles = Config.append_dir('NSAIDCCG')
	data = {}
	out = {}
	out['CCG'] = []
	out['Oct2012'] = []
	out['Oct2013'] = []
	out['Apr2013'] = []
	out['Jan2012'] = []
	out['Slope Diff (negated)'] = []
	out['Slope 1'] = []
	out['Inter 1'] = []
	out['Slope 2'] = []
	out['Inter 2'] = []
	out['Slope 3'] = []
	out['Inter 3'] = []
	out['Slope 1_lag'] = []
	out['Inter 1_lag'] = []
	out['Slope 2_lag'] = []
	out['Inter 2_lag'] = []
	out['Slope 3_lag'] = []
	out['Inter 3_lag'] = []

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
		out['CCG'].append(key)
		if len(value) == 22:
			inter_1, slope_1 = ts.LeastSquares(range(10),value[0:10])
			inter_2, slope_2 = ts.LeastSquares(range(10, 16),value[10:16])
			inter_3, slope_3 = ts.LeastSquares(range(16,22),value[16:22])
			inter_1_lag, slope_1_lag = ts.LeastSquares(range(11),value[0:11])
			inter_2_lag, slope_2_lag = ts.LeastSquares(range(11, 18),value[11:18])
			inter_3_lag, slope_3_lag = ts.LeastSquares(range(18,22),value[18:22])
			# x_1, y_1 = ts.FitLine(range(10), inter_1, slope_1)
			# x_2, y_2 = ts.FitLine(range(10, 22), inter_2, slope_2)
			# pyplot.plot(x_1, y_1,label='fit pre-guidance')
			# pyplot.plot(x_2, y_2, label='fit post-guidance')
			# pyplot.plot(value, label = 'actual percent diclofenac')
			# pyplot.title('percent diclophenac over time for CCG '+key)
			# pyplot.xlabel('months since Jan 2012')
			# pyplot.ylabel('percent diclophenac')
			# pyplot.show()
			slope_diff = slope_2 - slope_1

			out['Oct2012'].append(value[9])
			out['Oct2013'].append(value[21])
			out['Apr2013'].append(value[15])
			out['Jan2012'].append(value[0])
			out['Slope 1'].append(slope_1)
			out['Inter 1'].append(inter_1)
			out['Slope 2'].append(slope_2)
			out['Inter 2'].append(inter_2)
			out['Slope 3'].append(slope_3)
			out['Inter 3'].append(inter_3)
			out['Slope 1_lag'].append(slope_1_lag)
			out['Inter 1_lag'].append(inter_1_lag)
			out['Slope 2_lag'].append(slope_2_lag)
			out['Inter 2_lag'].append(inter_2_lag)
			out['Slope 3_lag'].append(slope_3_lag)
			out['Inter 3_lag'].append(inter_3_lag)
			out['Slope Diff (negated)'].append(-1*slope_diff)
		else:
			out['Oct2012'].append(None)
			out['Oct2013'].append(None)
			out['Apr2013'].append(None)
			out['Jan2012'].append(None)
			out['Slope Diff (negated)'].append(None)
			out['Slope 1'].append(None)
			out['Inter 1'].append(None)
			out['Slope 2'].append(None)
			out['Inter 2'].append(None)
			out['Slope 3'].append(None)
			out['Inter 3'].append(None)
			out['Slope 1_lag'].append(None)
			out['Inter 1_lag'].append(None)
			out['Slope 2_lag'].append(None)
			out['Inter 2_lag'].append(None)
			out['Slope 3_lag'].append(None)
			out['Inter 3_lag'].append(None)

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

def ClassifyCCGS1(Config):
	'''Conservative, uing intercept 1 and slope 2'''
	data = pandas.read_csv('Results/RateChange_NSAIDs.csv')
	data['Tot_Before'] = data['Inter 1'].map(lambda x: 'missing data' if x!=x else ('high' if x > .45 else ('low' if x < .2 else 'med')))
	data['Slope_After'] = data['Slope 2'].map(lambda x: 'missing data' if x!=x else ('up' if x > 0 else ('down' if x <-.005 else 'neutral')))
	data.to_csv('Results/RateChange_NSAIDs.csv',index=False)

def ClassifyCCGS2(Config):
	data = pandas.read_csv('Results/RateChange_NSAIDs.csv')
	data['Tot_Before'] = data['Jan2012'].map(lambda x: 'missing data' if x!=x else ('high' if x > .33 else ('low' if x < .25 else 'med')))
	data['Slope_After'] = data['Slope 2'].map(lambda x: 'missing data' if x!=x else ('up' if x > 0 else ('down' if x <-.01 else 'neutral')))
	data.to_csv('Results/RateChange_NSAIDs.csv',index=False)

def ClassifyCCGS3(Config):
	'''Using Oct 2012 and slope 2'''
	data = pandas.read_csv('Results/RateChange_NSAIDs.csv')
	data['Tot_Before'] = data['Oct2012'].map(lambda x: 'missing data' if x!=x else ('high' if x > .33 else ('low' if x < .25 else 'med')))
	data['Slope_After'] = data['Slope 2'].map(lambda x: 'missing data' if x!=x else ('up' if x > 0 else ('down' if x <-.01 else 'neutral')))
	data.to_csv('Results/RateChange_NSAIDs.csv',index=False)


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

	ax.set_xticklabels(['up','slightly down', 'significantly down'], minor=False)
	ax.set_yticklabels(column_labels, minor=False)
	pyplot.title('Number of CCG groups in each category')
	pyplot.ylabel('Initial prescribing rate of diclofenac vs. naproxen')
	pyplot.xlabel('change in diclofenac prescribing rate after directive')
	pyplot.show()

def plotContinuousClass(Config):
	'''
	plot slope after directive vs prescribing rate in Jan 2012 to viz clusters
	'''
	data = pandas.read_csv('Results/RateChange_NSAIDs.csv').to_dict(outtype='list')
	pyplot.scatter(data['Jan2012'],data['Slope 2'],alpha=.25, label = 'Oct 2012')
	pyplot.plot([0,1],[0,0],'k-',alpha=.5)
	pyplot.plot([0,1],[-.01,-.01],'k--',alpha=.5)
	pyplot.plot([.25,.25],[-.1,.1],'k--',alpha=.5)
	pyplot.plot([.33,.33],[-.1,.1],'k--',alpha=.5)
	# pyplot.scatter(data['Inter 1'],data['Slope 2'],color='blue', label = 'Jan 2012')
	# pyplot.legend()
	pyplot.axis([0,1,-.1,.06])
	pyplot.xlabel('percent diclofenac at Oct 2012',
		fontsize = 14)
	pyplot.ylabel('rate of change after directive\n(percent diclofenac/month)',
		fontsize = 14)
	pyplot.title('Diclofenac prescribing behavior \nat and after Oct 2012 by CCG group',
		fontsize=18)
	pyplot.show()

	# pyplot.scatter(data['Oct2012'],data['Oct2013'],alpha=.25)
	# pyplot.plot([0,1],[0,1],'k--', alpha=.5)
	# pyplot.axis([0,1,0,1])
	# pyplot.xlabel('percent diclofenac at Oct 2012',
	# 	fontsize = 14)
	# pyplot.ylabel('percent diclofenac at Oct 2013',
	# 	fontsize = 14)
	# pyplot.title('Diclofenac prescribing behavior \nfrom Oct 2012 to 12 months later by CCG group',
	# 	fontsize=18)
	# pyplot.show()

	# pyplot.scatter(data['Apr2013'],data['Oct2013'],alpha=.25)
	# pyplot.plot([0,1],[0,1],'k--', alpha=.5)
	# pyplot.axis([0,1,0,1])
	# pyplot.xlabel('percent diclofenac at Apr 2013',
	# 	fontsize = 14)
	# pyplot.ylabel('percent diclofenac at Oct 2013',
	# 	fontsize = 14)
	# pyplot.title('Diclofenac prescribing behavior \nfrom Apr to Oct 2013 by CCG group',
	# 	fontsize=18)
	# pyplot.show()

	pyplot.scatter(data['Slope 2'],data['Slope 3'],alpha=.5)
	pyplot.plot([0.015,-.042],[0.015,-.042],'k--', alpha=.5)
	pyplot.axis([-.042,.015,-.042,.015])
	pyplot.xlabel('Slope after directive (Oct 2012 to Apr 2013)',
		fontsize = 14)
	pyplot.ylabel('Slope after switch to CCGs (Apr 2013 to Oct 2013',
		fontsize = 14)
	pyplot.title('Effect of directive versus CCG management \non change in diclofenac prescriptions',
		fontsize=18)
	pyplot.show()

	pyplot.scatter(data['Slope 1'],data['Slope 2'],alpha=.5)
	pyplot.plot([0.015,-.042],[0.015,-.042],'k--', alpha=.5)
	pyplot.axis([-.042,.015,-.042,.015])
	pyplot.xlabel('Slope before directive (Jan 2012 to Oct 2012)',
		fontsize = 14)
	pyplot.ylabel('Slope after directive (Oct 2012 to Apr 2013)',
		fontsize = 14)
	pyplot.title('Effect of directive on change in diclofenac prescriptions',
		fontsize=18)
	pyplot.show()

	pyplot.scatter(data['Slope 2_lag'],data['Slope 3_lag'],alpha=.5)
	pyplot.plot([0.015,-.042],[0.015,-.042],'k--', alpha=.5)
	pyplot.axis([-.042,.015,-.042,.015])
	pyplot.xlabel('Slope after directive (Dec 2012 to Jul 2013)',
		fontsize = 14)
	pyplot.ylabel('Slope after switch to CCGs (Jul 2013 to Oct 2013',
		fontsize = 14)
	pyplot.title('Effect of directive versus CCG management \non change in diclofenac prescriptions (with lag)',
		fontsize=18)
	pyplot.show()

	pyplot.scatter(data['Slope 1_lag'],data['Slope 2_lag'],alpha=.5)
	pyplot.plot([0.015,-.042],[0.015,-.042],'k--', alpha=.5)
	pyplot.axis([-.042,.015,-.042,.015])
	pyplot.xlabel('Slope before directive (Jan 2012 to Dec 2012)',
		fontsize = 14)
	pyplot.ylabel('Slope after directive (Dec 2012 to Jul 2013)',
		fontsize = 14)
	pyplot.title('Effect of directive on change in diclofenac prescriptions (with lag)',
		fontsize=18)
	pyplot.show()

def projectedVsActualRate(Config):
	'''Demonstrate the difference between the Oct 2013 diclofenac 
	rate projected by pre-directive slopes, and the actual rate'''

	data = pandas.read_csv('Results/RateChange_NSAIDs.csv')
	data['sel'] = data.apply(lambda row: 0 if row['Oct2013'] != row['Oct2013'] else 1,axis=1)
	data = data[data['sel']==1]
	data.to_dict(outtype='list')

	projected = [inter + delta 
		for inter,delta 
		in zip(data['Inter 1'],[21*slope for slope in data['Slope 1']])]

	sortData = sorted(zip(data['Oct2013'],projected),key=lambda x: x[0])


	pyplot.plot([p for a,p in sortData],'b.',label='projected based on pre-directive behavior')
	pyplot.plot([a for a,p in sortData], 'r*', label='actual')
	pyplot.legend()
	pyplot.xlabel('CCGs', fontsize=14)
	pyplot.ylabel('Percent diclofenac at Oct 2013', fontsize=14)
	pyplot.title('Change in diclofenac prescribing rates', fontsize=18)
	pyplot.show()

def fitLine(xs,ys):
	inter, slope = ts.LeastSquares(xs,ys)
	res = ts.LogYResiduals(xs, ys, inter, slope)
	ybar, yvar = ts.MeanVar(ys)
	rbar,rvar = ts.MeanVar(res)
	sd_null,sd_fit = math.sqrt(yvar),math.sqrt(rvar)
	return inter, slope, sd_null, sd_fit


def plotUKOverTime(Config):
	'''plot percentage of diclofenac in britain each month'''
	infiles = Config.append_dir('NSAIDSummed')
	data = []

	for infile in infiles:
		df = pandas.read_csv(infile)
		dic = np.sum(df['days_prescribed_diclofenac'])
		nap = np.sum(df['days_prescribed_naproxen'])
		data = [dic/(nap+dic)] + data

	range1 = data[0:10]
	range2 = data[10:16]
	range3 = data[16:22]

	inter_1,slope_1,sd1_null,sd1_fit = fitLine(range(10),range1)
	inter_2,slope_2,sd2_null,sd2_fit = fitLine(range(10,16),range2)
	inter_3,slope_3,sd3_null,sd3_fit = fitLine(range(16,22),range3)

	pyplot.plot(range(10),range1,'r.',markersize=10)
	pyplot.plot(range(10, 16),range2,'b.',markersize=10)
	pyplot.plot(range(16,22),range3,'g.',markersize=10)
	pyplot.plot([9,9],[0,1],'k--', alpha = .3)
	pyplot.plot([15,15],[0,1],'k--', alpha = .3)
	pyplot.plot([0,22],[inter_1,inter_1+(22*slope_1)],
		'r--',
		alpha=.45, 
		label = 'projected from pre-directive')
	pyplot.plot([9,22],[inter_2+(9*slope_2),inter_2+(22*slope_2)],
		'b--',
		alpha=.45, 
		label = 'projected from post-directive (pre-CCG)')
	pyplot.plot([15,22],[inter_3+(15*slope_3),inter_3+(22*slope_3)],
		'g--',
		alpha=.45, 
		label = 'projected from post-CCGs')
	pyplot.legend()
	pyplot.axis([0,22,.15,.4])
	pyplot.xlabel('Months since Jan 2012', fontsize=14)
	pyplot.ylabel('Percent diclofenac prescribed', fontsize=14)
	pyplot.title('Average diclofenac prescribing rates in the UK',fontsize=18)
	pyplot.show()	

	print "Slope 1:", slope_1, "Deviation:", sd1_null, "vs.", sd1_fit
	print "Slope 2:", slope_2, "Deviation:", sd2_null, "vs.", sd2_fit
	print "Slope 3:", slope_3, "Deviation:", sd3_null, "vs.", sd3_fit
	print "Projected (before directive): ", (inter_1 + (21* slope_1))
	print "Projected (after directive):", (inter_2 + (21*slope_2))
	print "Projected (after directive):", (inter_3 + (21*slope_3))
	print "Actual: ", data[-1]

if __name__ == "__main__":
	Config = config.Config()
	# makeIndChange(Config)
	# makeIndChangePCT(Config)
	# ClassifyCCGS2(Config)
	# reportClass(Config)
	# plotContinuousClass(Config)
	plotUKOverTime(Config)
	# projectedVsActualRate(Config)

	