import pandas
import matplotlib.pyplot as pp
import config
import math
import util

def monthToInt(month):
	'''Returns the number (0-11) of a month given by 3 letters'''
	mons = {'Jan':0, 'Feb':1, 'Mar':2, 
			'Apr':3, 'May':4, 'Jun':5, 
			'Jul':6, 'Aug':7, 'Sep':8,
			'Oct':9, 'Nov':10, 'Dec':11}
	return mons[month]

def dateToInt(date):
	'''returns a decimal representation of the month and year'''
	return int(date[3:])+(monthToInt(date[:3])/12.0)

def mkPlotMedianStdDevs(data,color):
	'''plot the standard deviation in both 
	directions around the mean and the median'''
	data['Date'] = data['Date'].map(dateToInt)
	data['UpperSD'] = data['Mean']+data['StdDev']
	data['LowerSD'] = data['Mean']-data['StdDev']
	pp.plot(data['Date'],data['Median'], 
		linestyle='solid', color=color, marker='o')
	pp.plot(data['Date'],data['UpperSD'], 
		linestyle='dashed', color=color)
	pp.plot(data['Date'],data['LowerSD'], 
		linestyle='dashed', color=color)

def mkPlotMedianMean(data,color,name=''):
	'''plot the standard deviation in both 
	directions around the mean and the median'''
	data['Date'] = data['Date'].map(dateToInt)
	pp.plot(data['Date'],data['Median'], 
		linestyle='solid', color=color, marker='o', label=name+' Median')
	pp.plot(data['Date'],data['Mean'], 
		linestyle='solid', color=color, marker='*', label=name+' Mean')

def mkPlotComparison(data1,data2,data1label='',data2label=''):
	mkPlotMedianMean(data1,"red",name=data1label)
	mkPlotMedianMean(data2,"blue",name=data2label)

def mkPlotVersus(df,x,y,**args):
	data = df.to_dict(outtype='list')
	pp.scatter(data[x],data[y],**args)
	

if __name__ =="__main__":
	Config = config.Config()

	'''PPI items vs. cost'''

	# df_Brand = pandas.read_csv('SepBrand/Oct2013.csv')
	# df_Gen = pandas.read_csv('SepGeneric/Oct2013.csv')

	# df_Brand = util.sumBy(df_Brand,Config.keys['bnf'])
	# df_Gen = util.sumBy(df_Gen,Config.keys['bnf'])

	# df_Brand['cost'] = df_Brand[Config.keys['nic']]/df_Brand[Config.keys['quantity']]
	# df_Gen['cost'] = df_Gen[Config.keys['nic']]/df_Gen[Config.keys['quantity']]
	
	# mkPlotVersus(df_Brand,'cost',Config.keys['items'],color="red",label="Brand")
	# mkPlotVersus(df_Gen,'cost',Config.keys['items'],color="blue",label="Generic")
	# pp.title('PPIs (Oct 2013)')
	# pp.ylabel('Number of prescriptions for drug')
	# pp.xlabel('Drug Cost')
	# pp.legend()
	# pp.yscale('log')
	# pp.show()

	'''All Drugs items vs. cost'''
	data = pandas.read_csv('CompressedData/Oct2013.csv')
	data = util.sumBy(data,Config.keys['bnf'])
	data['cost'] = data[Config.keys['nic']]/data[Config.keys['quantity']]
	mkPlotVersus(data,'cost',Config.keys['items'])
	pp.title('All Drugs (Oct 2013)')
	pp.ylabel('Number of prescriptions for drug')
	pp.xlabel('Drug Cost')
	pp.xscale('log')
	pp.yscale('log')
	pp.axis([0.001, 3000, 0.1, 3200000])
	pp.show()


	'''
	df_Brand_Quan = pandas.read_csv('Results/SepBrand_Quantity_SummaryStats.csv')
	df_Gen_Quan = pandas.read_csv('Results/SepGeneric_Quantity_SummaryStats.csv')
	
	mkPlotComparison(df_Brand_Quan,df_Gen_Quan)
	pp.title('Median and Dist of Brand and Generic Over Time')
	pp.show()
	
	df = pandas.DataFrame.merge(df_Brand_Cost,df_Brand_Quan,on='Date',suffixes=('_c','_q'))
	pp.plot(df['Mean_c'],df['Mean_q'], 'ro')
	pp.plot(df['Median_c'],df['Median_q'], 'bo')
	pp.xlabel('Average cost of drugs in month')
	pp.ylabel('Average number prescribed in month')
	pp.show()
	'''