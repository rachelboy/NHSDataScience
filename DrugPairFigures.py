import config
import matplotlib.pyplot as plt
import pandas
import numpy

def loadDF(filename):
	print "Loading", filename
	try:
		return pandas.read_csv(filename)
	except:
		print "trouble loading", filename
		return False

def graph_drugs_line(items,nic):

	months = Config.filenames
	months = [x.strip('.csv') for x in months]
	months.reverse()

	for drug in items.keys():
		items_list = []
		nics=[]
		for month in months:
			try:
				items_list.append(items[drug][month])
				nics.append(nic[drug][month])
			except KeyError:
				print drug + ' not all information available'				
				break
		else:						 
			
			index = numpy.arange(len(months))
			graph = plt.plot(index, items_list, 'r.-', index, nics, 'g.-')
			
			lessMonths = [months[int(i)] for i in numpy.linspace(0,len(months)-1,num=6)]
			ax = plt.gca()
			plt.locator_params(nbins=len(lessMonths))
			ax.set_xticklabels(lessMonths)
			
			ax.set_ylabel('Branded/Generic')
			ax.set_title('Percent branded for chemical: '+drug)

			ax.legend( ('items', 'nic') )

			plt.savefig('Time_ChemPercents_figures/' + drug)
			plt.clf()

if __name__ == "__main__":
	Config = config.Config()

	folder = 'PpiDrugPairings'
	infiles = Config.append_dir(folder)

	items = {}
	nic = {}

	for month in infiles:
		df = loadDF(month)
		month = month[-11:-4]

		for index,row in df.iterrows():
			chem =row['ChemID']
			
			if chem in items.keys():
				items[chem][month] = (row['percent'+Config.keys['items']])#,row[Config.keys['nic']])
				nic[chem][month] = (row['percent'+Config.keys['nic']])#,row[Config.keys['nic']])

			else:
				items[chem] = {}
				items[chem][month] = (row['percent'+Config.keys['items']])#,row[Config.keys['nic']])
				
				nic[chem] = {}
				nic[chem][month] = (row['percent'+Config.keys['nic']])#,row[Config.keys['nic']])

	graph_drugs_line(items,nic)