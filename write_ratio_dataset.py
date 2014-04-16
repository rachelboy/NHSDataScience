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

class Write_ratio_CCGs(Pipeline):
	def run(self):
		bfile = self.Config.append_dir("WriteRatioDatasetBrand")
		gfile = self.Config.append_dir("WriteRatioDatasetGeneric")
		ofile = self.Config.append_dir("WriteRatioDatasetOut")

		for (brand, generic, outfile) in zip(bfile,gfile,ofile):
			brandfile = self.loadDF(brand)

			genericfile = self.loadDF(generic)

			
			groupedbrand = util.sumBy(brandfile,[self.Config.keys['pct'],self.Config.keys['ccg']])
			groupedgeneric = util.sumBy(genericfile,[self.Config.keys['pct'],self.Config.keys['ccg']])
			
			output = pandas.DataFrame.merge(
				groupedbrand, 
				groupedgeneric, 
				on=[self.Config.keys['pct'],self.Config.keys['ccg']],
				how = 'outer', 
				suffixes =('brand','generic'))

			items = self.Config.keys['items']
			quan = self.Config.keys['quantity']
			nic = self.Config.keys['nic']
			parts = [[items,quan,nic],['brand','generic']]
			drops = []

			for a in parts[0]:
				for b in parts[1]:
					output[a+b] = output[a+b].map(lambda x: 0 if x!=x else x)
					drops.append(a+b)
			drops = drops + ['INCLUDEbrand','GENERICbrand','INCLUDEgeneric',
					'GENERICgeneric']

			output['sumitems'] = output[items+'brand']+output[items+'generic']
			output['sumquantity'] = output[quan+'brand']+output[quan+'generic']
			output['sumnic'] = output[nic+'brand']+output[nic+'generic']

			output['percitems']= output[items+'brand']/output['sumitems']
			output['percquantity'] = output[quan+'brand']/output['sumquantity']
			output['percnic'] = output[nic+'brand']/output['sumnic']
			
			output = output.drop(drops,axis=1)

			output.to_csv(outfile, index = False)


class Write_ratio_dataset(Pipeline):
	def run(self):
		bfile = self.Config.append_dir("WriteRatioDatasetBrand")
		gfile = self.Config.append_dir("WriteRatioDatasetGeneric")
		ofile = self.Config.append_dir("WriteRatioDatasetOut")

		for (brand, generic, outfile) in zip(bfile,gfile,ofile):
			brandfile = self.loadDF(brand)
			# if not brandfile:
			# 	continue
			genericfile = self.loadDF(generic)
			# if not genericfile:
			# 	continue
			
			groupedbrand = util.sumBy(brandfile,[self.Config.keys['practice'],'postal code'])
			groupedgeneric = util.sumBy(genericfile,[self.Config.keys['practice'],'postal code'])
			
			output = pandas.DataFrame.merge(
				groupedbrand, 
				groupedgeneric, 
				on=self.Config.keys['practice'],
				how = 'outer', 
				suffixes =('brand','generic'))
			

			items = self.Config.keys['items']
			quan = self.Config.keys['quantity']
			nic = self.Config.keys['nic']
			parts = [[items,quan,nic],['brand','generic']]
			drops = []

			for a in parts[0]:
				for b in parts[1]:
					output[a+b] = output[a+b].map(lambda x: 0 if x!=x else x)
					drops.append(a+b)
			drops = drops+['INCLUDEbrand','GENERICbrand','INCLUDEgeneric',
					'GENERICgeneric','postal codebrand','postal codegeneric']

			output['postal code'] = output.apply(
				lambda row: row['postal codegeneric'] 
				if row['postal codebrand']!=row['postal codebrand'] 
				else row['postal codebrand'],
				axis=1)

			output['sumitems'] = output[items+'brand']+output[items+'generic']
			output['sumquantity'] = output[quan+'brand']+output[quan+'generic']
			output['sumnic'] = output[nic+'brand']+output[nic+'generic']

			output['ratioitems']= output[items+'brand']/output['sumitems']
			output['ratioquantity'] = output[quan+'brand']/output['sumquantity']
			output['rationic'] = output[nic+'brand']/output['sumnic']
			
			output = output.drop(drops,axis=1)

			output.to_csv(outfile, index = False)


class JoinAndAggByOutCode(Pipeline):
	def run(self):
		infiles = self.Config.append_dir("OutCodeRatiosIn")
		outfiles = self.Config.append_dir("OutCodeRatiosOut")

		outcodes = self.loadDF('postcodes.csv')
		if not outcodes:
			return

		for infile,outfile in zip(infiles,outfiles):
			data = self.loadDF(infile)
			if not data:
				continue

			labels = ['items','quantity','nic']
			for a in labels:
				data['tot'+a] = data['sum'+a]*data['ratio'+a]
			print data
			print data['postal code']
			data['outcode'] = data['postal code'].map(lambda x: x.partition(' ')[0])
			data = util.sumBy(data,'outcode')
			for a in labels:
				data['ratio'+a] = data['tot'+a]/data['sum'+a]
				data.drop('tot'+a,axis=1)
			data = pandas.DataFrame.merge(data,outcodes,on='outcode',how='left')
			data.to_csv(outfile)


if __name__ == "__main__":
	Config = config.Config()
	
	# next = Write_ratio_dataset(Config)
	# next.run()

	# next = JoinAndAggByOutCode(Config)
	# next.run()
	
	next = Write_ratio_CCGs(Config)
	next.run()