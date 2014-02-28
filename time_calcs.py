import util
import config
import pandas
import os
from matplotlib import pyplot as plt
import numpy 
import matplotlib


def loadDF(filename):
	print "Loading", filename
	try:
		return pandas.read_csv(filename)
	except:
		print "trouble loading", filename
		return False


def calc_drug_over_time(Config):
	folder = 'SepGeneric'
	infiles = Config.append_dir(folder)

	quantity = {}
	nic = {}

	for month in infiles:
		df = loadDF(month)
		month = month[-11:-4]
		grouped = util.sumBy(df,Config.keys['bnf'])

		for index,row in grouped.iterrows():
			item =row[Config.keys['bnf']]
			
			if item in quantity.keys():
				quantity[item][month] = (row[Config.keys['quantity']])#,row[Config.keys['nic']])
				nic[item][month] = (row[Config.keys['nic']])#,row[Config.keys['nic']])

			else:
				quantity[item] = {}
				quantity[item][month] = (row[Config.keys['quantity']])#,row[Config.keys['nic']])
				
				nic[item] = {}
				nic[item][month] = (row[Config.keys['nic']])#,row[Config.keys['nic']])

	return quantity,nic
def graph_drugs(dics,drug):
	quantity, nic = dics

	months = Config.filenames
	months = [x.strip('.csv') for x in months]
	
	quantities = []
	nics=[]

	for month in months:
		quantities.append(quantity[drug][month])

	for month in months:
		nics.append(nic[drug][month])

	months.reverse()
	print months
	ind = numpy.arange(len(months))  # the x locations for the groups
	width = .2
	fig, ax = plt.subplots()
	rects1 = ax.bar(ind, quantities, width, color='r')
	rects2 = ax.bar(ind+width, nics, width, color='y')

	# add some
	ax.set_ylabel('Sum')
	ax.set_title('Sum of quantity and nic for bnf code: '+drug)
	ax.set_xticks(ind+width)
	ax.set_xticklabels(months)

	ax.legend( (rects1[0], rects2[0]), ('quantity', 'nic') )



	# plt.bar(range(len(quantity[drug])), quantity[drug].values(), align='center')
	# plt.xticks(range(len(quantity[drug])), quantity[drug].keys())



	plt.show()

def graph_drugs_line(dics,drug):
	quantity, nic = dics

	months = Config.filenames
	months = [x.strip('.csv') for x in months]
	
	quantities = []
	nics=[]
	
	for month in months:
		quantities.append(quantity[drug][month])

	for month in months:
		nics.append(nic[drug][month])
	print quantities
	print nics
	costs = [y/x for x,y in zip(quantities,nics)]
 
	months.reverse()
	index = numpy.arange(len(months))
	graph = plt.plot(index, quantities, 'r.-', index, nics, 'g.-', index, costs, 'b.-')
	ax = plt.gca()
	ax.set_xticklabels(months)
	
	ax.set_ylabel('Sum')
	ax.set_title('Sum of quantity, nic and cost for bnf code: '+drug)


	ax.legend( ('quantity', 'nic', 'cost') )



	# plt.bar(range(len(quantity[drug])), quantity[drug].values(), align='center')
	# plt.xticks(range(len(quantity[drug])), quantity[drug].keys())



	plt.show()


if __name__ == "__main__":

	Config = config.Config()
	drug = calc_drug_over_time(Config)
	graph_drugs_line(drug,'0103050P0AABDBD')



