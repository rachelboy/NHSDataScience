import config
import pandas
import numpy as np
import thinkstats as ts
import thinkplot as tp
import util
import math

def makeDrugSums(filename,Config):
	'''returns dataframe from file, aggregated by bnf code'''
	df = pandas.read_csv(filename)
	df = util.sumBy(df,Config.keys['bnf'])
	return df

def plotLogNormal(data,key,bins = False):
	'''plot normal and log pmf and cdf
	bins - optional argument, number of bins to put pmf data in
	'''
	if type(data) == str:
		data = pandas.read_csv(data).to_dict(outtype='list')
	else:
		data = data.to_dict(outtype='list')
	d = data[key]
	cdf = ts.MakeCdfFromList(d)
	if bins:
		d = BinData(d,np.min(d),np.max(d),bins)
	pmf = ts.MakePmfFromList(d)

	tp.SubPlot(2, 2, 1)
	tp.Pmf(pmf)
	tp.Config(title='linear pmf')

	tp.SubPlot(2, 2, 2)
	tp.Pmf(pmf)
	scale={'xscale':'log','yscale':'log'}
	tp.Config(title='logx pmf',**scale)

	tp.SubPlot(2, 2, 3)
	scale = tp.Cdf(cdf, xscale='linear')
	tp.Config(title='linear cdf', **scale)	

	tp.SubPlot(2, 2, 4)
	scale = tp.Cdf(cdf, xscale='log')
	tp.Config(title='logx cdf', **scale)

	tp.Show()

def CompCdf(dataList,keyList,nameList,colorList,title = '',xlabel = '',xscale='linear'):
	'''plot cdfs of all data, key pairs with given parameters'''
	for data,key,name,color in zip(dataList,keyList,nameList,colorList):
		d = data.to_dict(outtype='list')
		cdf = ts.MakeCdfFromList(d[key])

		scale = tp.Cdf(cdf, xscale=xscale, label=name, color = color)
	tp.Config(legend=True, 
		title=title, 
		xlabel = xlabel, 
		**scale)	
	tp.Show()


def BinData(data, low, high, n):
    """Rounds data off into bins.

    data: sequence of numbers
    low: low value
    high: high value
    n: number of bins

    returns: sequence of numbers
    """
    bins = np.linspace(low, high, n)
    data = (np.array(data) - low) / (high - low) * n
    data = np.round(data) * (high - low) / n + low
    return data


if __name__ == "__main__":
	Config = config.TestConfig()
	
	data = pandas.read_csv('JoinedPpis/Oct2013.csv')
	data = util.sumBy(data,Config.keys['bnf'])
	data['cost'] = data[Config.keys['nic']]/data[Config.keys['quantity']]
	
	'''
	data = pandas.read_csv('RatioDataset/Oct2013.csv')
	labels = ['items','quantity','nic']
	for a in labels:
		data['tot'+a] = data['sum'+a]*data['ratio'+a]
	data['outcode'] = data['postal code'].map(lambda x: x.partition(' ')[0])
	data = util.sumBy(data,'outcode')
	for a in labels:
		data['ratio'+a] = data['tot'+a]/data['sum'+a]
		data.drop('tot'+a,axis=1)
	'''
	plotLogNormal(data,Config.keys['quantity'], bins = None)



	'''
	print 'All Drugs (Cost)'
	df = makeDrugSums("CompressedData/Oct2013.csv", Config)
	df['cost'] = df[Config.keys['nic']]/df[Config.keys['quantity']]
	util.plotLogNormal(df,'cost')
	
	print 'All PPIs (Cost)'
	df = makeDrugSums("JoinedPpis/Oct2013.csv", Config)
	df['cost'] = df[Config.keys['nic']]/df[Config.keys['quantity']]
	util.plotEverything(df,'cost')

	print 'Brand PPIs (Cost)'
	df = makeDrugSums("SepBrand/Oct2013.csv", Config)
	df['cost'] = df[Config.keys['nic']]/df[Config.keys['quantity']]
	util.plotEverything(df,'cost')
	
	print 'Generic PPIs (Cost)'
	df = makeDrugSums("SepGeneric/Oct2013.csv", Config)
	df['cost'] = df[Config.keys['nic']]/df[Config.keys['quantity']]
	util.plotEverything(df,'cost')
	
	infolders = ['JoinedPpis','SepBrand','SepGeneric']
	infiles = [name+'/Oct2013.csv' for name in infolders]

	dfs = [makeDrugCosts(fin,Config) for fin in infiles]
	CompCdf(dfs,
		[Config.keys['nic'] for i in range(len(dfs))],
		infolders,
		['black','red','blue'],
		title = 'CDF of expenditures per drug (Oct 2013)',
		xlabel = 'Total expenditure',
		xscale = 'log')
	'''


	
