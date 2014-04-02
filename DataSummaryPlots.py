import config
import util
import matplotlib.pyplot as pyplot
import numpy as np
import pandas
import thinkstats as ts
import thinkplot as tp

def plotLogNormal(data,key,res=1000):
	'''plot normal and log pmf and cdf
	bins - optional argument, number of bins to put pmf data in
	'''
	if type(data) == str:
		data = pandas.read_csv(data).to_dict(outtype='list')
	else:
		data = data.to_dict(outtype='list')
	d = data[key]
	cdf = ts.MakeCdfFromList(d)
	pdf = ts.EstimatedPdf(d)
	pmf = pdf.MakePmf(np.linspace(np.min(d),np.max(d),num=res))

	tp.SubPlot(2, 2, 1)
	tp.Pmf(pmf)
	tp.Config(title='linear pmf')

	tp.SubPlot(2, 2, 2)
	tp.Pmf(pmf)
	scale={'xscale':'log','yscale':'linear'}
	tp.Config(title='logx pmf',**scale)

	tp.SubPlot(2, 2, 3)
	scale = tp.Cdf(cdf, xscale='linear')
	tp.Config(title='linear cdf', **scale)	

	tp.SubPlot(2, 2, 4)
	scale = tp.Cdf(cdf, xscale='log')
	tp.Config(title='logx cdf', **scale)

	tp.Show()

def plotLogCDF(data,key,title,ylabel,xlabel):
	cdf = ts.MakeCdfFromList(data.to_dict(outtype='list')[key])
	scale = tp.Cdf(cdf, xscale='log')
	tp.Config(title = title, ylabel=ylabel, xlabel=xlabel, **scale)
	tp.Show()

def plotMultipleLogCDF(datas,key,title,ylabel,xlabel):
	for data in datas:
		cdf = ts.MakeCdfFromList(data[1].to_dict(outtype='list')[key])
		scale = tp.Cdf(cdf, xscale='log', label=data[2])
	tp.Config(title = title, ylabel=ylabel, xlabel=xlabel, **scale)
	tp.Show()

def plotLinearCDF(data,key,title,ylabel,xlabel):
	cdf = ts.MakeCdfFromList(data.to_dict(outtype='list')[key])
	scale = tp.Cdf(cdf, xscale='linear')
	tp.Config(title = title, axis=[0,300000,0,1], 
		ylabel=ylabel, xlabel=xlabel, **scale)
	tp.Show()



if __name__ == "__main__":
	Config = config.Config()

	# infiles = Config.append_dir('NSAIDCCG')
	# data = {}
	# data['mean'] = []
	# data['dev_up'] = []
	# data['dev_down'] = []
	# for infile in infiles:
	# 	mon = pandas.read_csv(infile)
	# 	mean = np.mean(mon['percent'])
	# 	std_dev = np.std(mon['percent'])
	# 	data['mean'] = [mean] + data['mean']
	# 	data['dev_up'] = [mean+std_dev] + data['dev_up']
	# 	data['dev_down'] = [mean-std_dev] + data['dev_down']

	# 	'''
	# 	for index,row in mon.iterrows():
	# 		data[row['CCG']] = [row['percent']] + data.get(row['CCG'],[]) 
	# for key, value in data.items():
	# 	pyplot.plot(value)
	# '''
	# pyplot.plot(data['mean'], label = 'average')
	# pyplot.plot(data['dev_up'],'.', label = '1 std dev up')
	# pyplot.plot(data['dev_down'],'.', label = '1 std dev down')
	# pyplot.legend()
	# pyplot.title('Averge percent diclofenac over all CCGs (Jan 2012 to Oct 2013)')
	# pyplot.ylabel('Percent diclofenac')
	# pyplot.xlabel('Months since Jan 2012')
	# pyplot.show()

	infile = Config.nsaid_directories['Ingest_out_nap']+'/Oct2013.csv'
	data = pandas.read_csv(infile)
	data = util.sumBy(data,Config.keys['bnf'])
	plotLogCDF(data,
		'days_prescribed',
		'Log(x) CDF of days prescribed for NSAID preparations (Oct 2013)',
		'','Days prescribed')


	# infile = Config.directories['Ingest_out']+'/Oct2013.csv'
	# data = pandas.read_csv(infile)
	# data = util.sumBy(data,Config.keys['bnf'])
	# plotLogCDF(data,
	# 	Config.keys['items'],
	# 	'Log(x) CDF of items for all drug preparations (Oct 2013)',
	# 	'','Prescriptions filled')
	# data['cost'] = data[Config.keys['nic']]/data[Config.keys['quantity']]
	# plotLogCDF(data,
	# 	'cost',
	# 	'Log(x) CDF of cost per unit for all drug preparations (Oct 2013)',
	# 	'','Cost per unit (eg pill)')


	# infile = Config.directories['Join_ppis_out']+'/Oct2013.csv'
	# data = pandas.read_csv(infile)
	# data = util.sumBy(data,Config.keys['bnf'])
	# plotLogCDF(data,
	# 	Config.keys['items'],
	# 	'Log(x) CDF of items for all PPIs (Oct 2013)',
	# 	'','Prescriptions filled')
	# data['cost'] = data[Config.keys['nic']]/data[Config.keys['quantity']]
	# plotLogCDF(data,
	# 	'cost',
	# 	'Log(x) CDF of cost per unit for all PPIs (Oct 2013)',
	# 	'','Cost per unit (eg pill)')

	# infile = Config.directories['Sep_brand_out']+'/Oct2013.csv'
	# data = pandas.read_csv(infile)
	# data = util.sumBy(data,Config.keys['bnf'])
	# plotLogCDF(data,
	# 	Config.keys['items'],
	# 	'Log(x) CDF of items for branded PPIs (Oct 2013)',
	# 	'','Prescriptions filled')
	# data['cost'] = data[Config.keys['nic']]/data[Config.keys['quantity']]
	# plotLogCDF(data,
	# 	'cost',
	# 	'Log(x) CDF of cost per unit for branded PPIs (Oct 2013)',
	# 	'','Cost per unit (eg pill)')



	# infile = Config.directories['Sep_generic_out']+'/Oct2013.csv'
	# data = pandas.read_csv(infile)
	# data = util.sumBy(data,Config.keys['bnf'])
	# plotLogCDF(data,
	# 	Config.keys['items'],
	# 	'Log(x) CDF of items for generic PPIs (Oct 2013)',
	# 	'','Prescriptions filled')
	# data['cost'] = data[Config.keys['nic']]/data[Config.keys['quantity']]
	# plotLogCDF(data,
	# 	'cost',
	# 	'Log(x) CDF of cost per unit for generic PPIs (Oct 2013)',
	# 	'','Cost per unit (eg pill)')

	# infile = 'NSAIDCCG/Oct2013.csv'
	# data = pandas.read_csv(infile)
	# data['days_prescribed_naproxen'] = data['days_prescribed_naproxen'].map(lambda x: 0 if x != x else x)
	# data['days_prescribed_diclofenac'] = data['days_prescribed_diclofenac'].map(lambda x: 0 if x != x else x)
	# plotLinearCDF(data,
	# 	'days_prescribed_naproxen',
	# 	'Days of naproxen prescribed by CCG (Oct2013)',
	# 	'Portion of CCGs prescribing at or below this rate',
	# 	'Days of naproxen prescribed')
	# plotLinearCDF(data,
	# 	'days_prescribed_diclofenac',
	# 	'Days of diclofenac prescribed by CCG (Oct2013)',
	# 	'Portion of CCGs prescribing at or below this rate',
	# 	'Days of diclofenac prescribed')

	# infile = 'NSAIDCCG/Jan2012.csv'
	# data = pandas.read_csv(infile)
	# data['days_prescribed_naproxen'] = data['days_prescribed_naproxen'].map(lambda x: 0 if x != x else x)
	# data['days_prescribed_diclofenac'] = data['days_prescribed_diclofenac'].map(lambda x: 0 if x != x else x)
	# plotLinearCDF(data,
	# 	'days_prescribed_naproxen',
	# 	'Days of naproxen prescribed by CCG (Jan2012)',
	# 	'Portion of CCGs prescribing at or below this rate',
	# 	'Days of naproxen prescribed')
	# plotLinearCDF(data,
	# 	'days_prescribed_diclofenac',
	# 	'Days of diclofenac prescribed by CCG (Jan2012)',
	# 	'Portion of CCGs prescribing at or below this rate',
	# 	'Days of diclofenac prescribed')
