import config
import util
import matplotlib.pyplot as pyplot
import numpy as np
import pandas
import thinkstats as ts
import thinkplot as tp
import random

def getPercents(summed):
	summed['perc0'] = summed['days_prescribed_diclofenac']/(summed['days_prescribed_naproxen']+summed['days_prescribed_diclofenac'])
	for i in range(1,6):
		summed['perc'+str(i)] = summed['days_prescribed_diclofenac'+str(i)]/(summed['days_prescribed_naproxen'+str(i)]+summed['days_prescribed_diclofenac'+str(i)])

def findSlopes(percented):
	slopes = []
	for i,r in percented.iterrows():
		trend = [r['perc'+str(j)] for j in range(6)]
		inter, slope = ts.LeastSquares(range(6),trend)
		slopes.append(slope)
	percented['slopes'] = slopes
	slopes = [s for s in slopes if not np.isnan(s)]

	return slopes

def findSlopeMeanVar(base):
	summed = util.sumBy(base,'CCG')

	getPercents(summed)
	slopes = findSlopes(summed)

	return ts.MeanVar(slopes)

def slopePVal(base, n):
	mean, var = findSlopeMeanVar(base)
	# print var
	CCGs = base.to_dict(outtype='list')['CCG']
	p = 0.0
	for i in range(n):
		random.shuffle(CCGs)
		base['CCG'] = CCGs
		mean2,var2 = findSlopeMeanVar(base)
		# print var2
		if var2 >= var:
			p += 1
	return p/n

def findFinalMeanVar(data):
	summed = util.sumBy(data,'CCG')
	summed['perc'] = summed['days_prescribed_diclofenac']/(summed['days_prescribed_naproxen']+summed['days_prescribed_diclofenac'])
	
	return ts.MeanVar(summed['perc'])

def finalPVal(data,n):
	CCGs = data.to_dict(outtype='list')['CCG']

	mean,var = findFinalMeanVar(data)
	p = 0.0
	
	for i in range(n):
		random.shuffle(CCGs)
		data['CCG'] = CCGs
		mean2,var2 = findFinalMeanVar(data)
		# print var, " ", var2
		if var2 >= var:
			p += 1
	return p/n

def plotFinalHists(data):
	data['days_prescribed_diclofenac'] = data['days_prescribed_diclofenac'].map(lambda x: 0 if x!=x else x)
	data['days_prescribed_naproxen'] = data['days_prescribed_naproxen'].map(lambda x: 0 if x!=x else x)
	summed = util.sumBy(data,'CCG')
	summed['perc'] = summed['days_prescribed_diclofenac']/(summed['days_prescribed_naproxen']+summed['days_prescribed_diclofenac'])
	pyplot.hist(summed['perc'], bins = 100)
	pyplot.title('Actual distribution of rate of diclophenac prescription',
		fontsize = 18)
	pyplot.xlabel('percent diclofenac prescribed', fontsize = 14)
	pyplot.ylabel('number of CCGs', fontsize = 14)
	pyplot.axis([0, 1, 0, 30])
	pyplot.show()

	CCGs = data.to_dict(outtype='list')['CCG']
	random.shuffle(CCGs)
	data['CCG'] = CCGs
	summed = util.sumBy(data,'CCG')
	summed['perc'] = summed['days_prescribed_diclofenac']/(summed['days_prescribed_naproxen']+summed['days_prescribed_diclofenac'])
	pyplot.hist(summed['perc'], bins = 100)
	pyplot.title('Example distribution of rate of diclofenac \nprescription without governance or geographic effect',
		fontsize = 18)
	pyplot.xlabel('percent diclofenac prescribed', fontsize = 14)
	pyplot.ylabel('number of CCGs', fontsize = 14)
	pyplot.axis([0, 1, 0, 30])
	pyplot.show()

def plotSlopeHists(data):
	summed = util.sumBy(data,'CCG')
	getPercents(summed)
	slopes = findSlopes(summed)
	pyplot.hist(slopes, bins = 50)
	pyplot.title('Actual distribution of rate of change \n of diclophenac prescription',
		fontsize = 18)
	pyplot.xlabel('rate of change of percent diclofenac prescribed', fontsize = 14)
	pyplot.ylabel('number of CCGs', fontsize = 14)
	pyplot.axis([-.06, .08, 0, 38])
	pyplot.show()

	CCGs = data.to_dict(outtype='list')['CCG']
	random.shuffle(CCGs)
	data['CCG'] = CCGs
	summed = util.sumBy(data,'CCG')
	getPercents(summed)
	slopes = findSlopes(summed)
	pyplot.hist(slopes, bins = 50)
	pyplot.title('Example distribution of rate of change \n of diclofenac prescription without \ngovernance or geographic effect',
		fontsize = 18)
	pyplot.xlabel('rate of change of percent diclofenac prescribed', fontsize = 14)
	pyplot.ylabel('number of CCGs', fontsize = 14)
	pyplot.axis([-.06, .08, 0, 38])
	pyplot.show()

def plotSlopeCDF(data):
	summed = util.sumBy(data,'CCG')
	getPercents(summed)
	slopes = findSlopes(summed)
	cdf1 = ts.MakeCdfFromList(slopes)
	pmf1 = ts.EstimatedPdf(slopes).MakePmf([x/200.0 for x in range(-12,21)])
	
	CCGs = data.to_dict(outtype='list')['CCG']
	random.shuffle(CCGs)
	data['CCG'] = CCGs
	summed = util.sumBy(data,'CCG')
	getPercents(summed)
	slopes = findSlopes(summed)
	cdf2 = ts.MakeCdfFromList(slopes)
	pmf2 = ts.EstimatedPdf(slopes).MakePmf([x/200.0 for x in range(-12,21)])

	pyplot.subplot(1,2,1)
	xs,ys = cdf1.Render()
	pyplot.plot(xs,ys,'r-',linewidth=2,label = 'Actual')
	xs,ys = cdf2.Render()
	pyplot.plot(xs,ys,'b--',linewidth=2,label='No CCG correlation')

	pyplot.xlabel('rate of change of percent diclofenac prescribed', fontsize = 14)
	pyplot.ylabel('fraction of CCGs at or below rate', fontsize = 14)
	pyplot.legend(loc=4)

	pyplot.subplot(1,2,2)
	xs,ys = pmf1.Render()
	pyplot.plot(xs,ys,'r-',linewidth=2,label = 'Actual')
	xs,ys = pmf2.Render()
	pyplot.plot(xs,ys,'b--',linewidth=2,label = 'No CCG correlation')

	# pyplot.title('Actual distribution of rate of change\nof diclophenac prescription compared to\ndistribtuion without any CCG correlation ',
	# 	fontsize = 18)
	pyplot.xlabel('rate of change of percent diclofenac prescribed', fontsize = 14)
	pyplot.ylabel('probability density', fontsize = 14)
	pyplot.legend(loc=1)
	pyplot.show()

def plotFinalCDF(data):
	data['days_prescribed_diclofenac'] = data['days_prescribed_diclofenac'].map(lambda x: 0 if x!=x else x)
	data['days_prescribed_naproxen'] = data['days_prescribed_naproxen'].map(lambda x: 0 if x!=x else x)
	summed = util.sumBy(data,'CCG')
	summed['perc'] = summed['days_prescribed_diclofenac']/(summed['days_prescribed_naproxen']+summed['days_prescribed_diclofenac'])
	cdf1 = ts.MakeCdfFromList(summed['perc'])
	pmf1 = ts.EstimatedPdf(summed['perc']).MakePmf([x/50.0 for x in range(51)])
	

	CCGs = data.to_dict(outtype='list')['CCG']
	random.shuffle(CCGs)
	data['CCG'] = CCGs
	summed = util.sumBy(data,'CCG')
	summed['perc'] = summed['days_prescribed_diclofenac']/(summed['days_prescribed_naproxen']+summed['days_prescribed_diclofenac'])
	cdf2 = ts.MakeCdfFromList(summed['perc'])
	pmf2 = ts.EstimatedPdf(summed['perc']).MakePmf([x/50.0 for x in range(51)])

	pyplot.subplot(1,2,1)
	xs,ys = cdf1.Render()
	pyplot.plot(xs,ys,'r-',linewidth=2,label = 'Actual')
	xs,ys = cdf2.Render()
	pyplot.plot(xs,ys,'b--',linewidth=2,label = 'No CCG correlation')

	pyplot.title('CDF')
	# pyplot.title('Actual distribution of percent diclofenac prescribed\ncompared to distribution with no CCG correlation',
		# fontsize = 18)
	pyplot.xlabel('percent diclofenac prescribed', fontsize = 14)
	pyplot.ylabel('fraction of CCGs at or below percentage', fontsize = 14)
	pyplot.legend(loc=4)
	pyplot.axis([0, 1, 0, 1])
	
	pyplot.subplot(1,2,2)
	xs,ys = pmf1.Render()
	pyplot.plot(xs,ys,'r-',linewidth=2,label = 'Actual')
	xs,ys = pmf2.Render()
	pyplot.plot(xs,ys,'b--',linewidth=2,label = 'No CCG correlation')

	pyplot.title('PDF')
	# pyplot.title('Actual distribution of percent diclofenac prescribed\ncompared to distribution with no CCG correlation',
		# fontsize = 18)
	pyplot.xlabel('percent diclofenac prescribed', fontsize = 14)
	pyplot.ylabel('probability density', fontsize = 14)
	pyplot.legend(loc=1)
	pyplot.show()

if __name__ == "__main__":
	Config = config.Config()
	infiles = Config.append_dir('NSAIDSummed')

	# base = pandas.read_csv(infiles[-6])

	# i = 0
	# for infile in infiles[-5:]:
	# 	i+=1
	# 	data = pandas.read_csv(infile)
	# 	data = data.drop(['PCT','CCG'], axis=1)
	# 	data['days_prescribed_diclofenac'] = data['days_prescribed_diclofenac'].map(lambda x: 0 if x!=x else x)
	# 	data['days_prescribed_naproxen'] = data['days_prescribed_naproxen'].map(lambda x: 0 if x!=x else x)
	
	# 	base = pandas.merge(base,data,on=Config.keys['practice'],suffixes=('',str(i)),sort=False)

	# plotSlopeCDF(base)

	data = pandas.read_csv(infiles[-1])
	plotFinalCDF(data)

	# print "slope", slopePVal(base,100)

	# data = pandas.read_csv(infiles[-1])
	
	# print "final perc", finalPVal(data,1000)

	# plotFinalHists(data)


	
