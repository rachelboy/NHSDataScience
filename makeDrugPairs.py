'''first 11 (10?) give same thing, different administrations (tab vs cap vs gran sach)
first 9 (8?) give chemically same, different names'''

import config
import util
import pandas
from os.path import expanduser
import os

class Pipeline(object):
	def __init__(self,Config):
		self.Config = Config


	def loadDF(self,filename):
		print "Loading", filename
		try:
			return pandas.read_csv(filename, index_col = False)
		except:
			print "trouble loading", filename, "in", self.Config.data_directory
			return False
class Make_drug_pairs(Pipeline):
	def run(self):
		infiles = self.Config.append_dir("MakeDrugPairsIn")
		outfiles = self.Config.append_dir("MakeDrugPairsOut")

		for (infile,outfile) in zip(infiles,outfiles):
			data = self.loadDF(infile)
			if not data:
				continue
			
			data['ChemID'] = data[self.Config.keys['bnf']].map(lambda x: x[0:9])
			data = util.sumBy(data,[self.Config.keys['practice'],'ChemID',self.Config.keys['gen'],'postal code'])
			
			grouped = pandas.groupby(data,self.Config.keys['gen'])
			data = pandas.merge(grouped.get_group(1.0),grouped.get_group(0.0),
				on =[self.Config.keys['practice'],'ChemID'], 
				left_index=False, 
				right_index = False,
				how = 'outer',
				sort = False,
				suffixes = ('_gen','_brand'))

			for col in data.columns.values.tolist():
				data[col] = data[col].map(lambda x: 0 if x!=x else x)

			data['postal code'] = data.apply(
				lambda row: row['postal code_gen'] 
				if row['postal code_brand']!=row['postal code_brand'] 
				else row['postal code_brand'],
				axis=1)

			items = self.Config.keys['items']
			quan = self.Config.keys['quantity']
			nic = self.Config.keys['nic']
			cols = [items,quan,nic]

			for col in cols:
				data['sum'+col] = data[col+'_brand']+data[col+'_gen']
				data['percent'+col]= data[col+'_brand']/data['sum'+col]

			data = data.drop(['INCLUDE_gen','INCLUDE_brand',
				'GENERIC_gen','GENERIC_brand',
				'postal code_gen','postal code_brand'], 
				axis=1)

			data.to_csv(outfile, index = False)


class JoinAndAggByOutCode(Pipeline):
	def run(self):
		infiles = self.Config.append_dir("OutCodeDrugsIn")
		outfiles = self.Config.append_dir("OutCodeDrugsOut")

		outcodes = self.loadDF('postcodes.csv')
		if not outcodes:
			return

		for infile,outfile in zip(infiles,outfiles):
			data = self.loadDF(infile)
			if not data:
				continue

			data['outcode'] = data['postal code'].map(lambda x: x.partition(' ')[0])
			data = util.sumBy(data,['outcode','ChemID'])

			items = self.Config.keys['items']
			quan = self.Config.keys['quantity']
			nic = self.Config.keys['nic']
			cols = [items,quan,nic]

			for col in cols:
				data['sum'+col] = data[col+'_brand']+data[col+'_gen']
				data['percent'+col]= data[col+'_brand']/data['sum'+col]
				data = data.drop([col+'_brand',col+'_gen'],axis=1)
			data = pandas.DataFrame.merge(data,outcodes,on='outcode',how='left')
			data.to_csv(outfile, index=False)

class JoinAndAggAll(Pipeline):
	def run(self):
		infiles = self.Config.append_dir("AllDrugsIn")
		outfiles = self.Config.append_dir("AllDrugsOut")

		for infile,outfile in zip(infiles,outfiles):
			data = self.loadDF(infile)
			if not data:
				continue

			data = util.sumBy(data,['ChemID'])

			items = self.Config.keys['items']
			quan = self.Config.keys['quantity']
			nic = self.Config.keys['nic']
			cols = [items,quan,nic]

			for col in cols:
				data['sum'+col] = data[col+'_brand']+data[col+'_gen']
				data['percent'+col]= data[col+'_brand']/data['sum'+col]
				data = data.drop([col+'_brand',col+'_gen'],axis=1)

			data.to_csv(outfile, index=False)


if __name__ == "__main__":
	Config = config.Config()
	
	next = Make_drug_pairs(Config)
	next.run()

	next = JoinAndAggByOutCode(Config)
	next.run()

	next = JoinAndAggAll(Config)
	next.run()
