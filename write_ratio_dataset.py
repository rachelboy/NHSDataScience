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
class Write_ratio_dataset(Pipeline):
	def run(self):
		bfile = self.Config.append_dir("WriteRatioDatasetBrand")
		gfile = self.Config.append_dir("WriteRatioDatasetGeneric")
		ofile = self.Config.append_dir("WriteRatioDatasetOut")

		for (brand, generic, outfile) in zip(bfile,gfile,ofile):
			brandfile = self.loadDF(brand)
			genericfile = self.loadDF(generic)
			
			groupedbrand = util.sumBy(brandfile,self.Config.keys['practice'])
			groupedgeneric = util.sumBy(genericfile,self.Config.keys['practice'])
			
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
			drops = drops+['INCLUDEbrand','GENERICbrand','INCLUDEgeneric','GENERICgeneric']

			output['sumitems'] = output[items+'brand']+output[items+'generic']
			output['sumquantity'] = output[quan+'brand']+output[quan+'generic']
			output['sumnic'] = output[nic+'brand']+output[nic+'generic']

			

			output['ratioitems']= output[items+'brand']/output['sumitems']
			output['ratioquantity'] = output[quan+'brand']/output['sumquantity']
			output['rationic'] = output[nic+'brand']/output['sumnic']
			
			output = output.drop(drops,axis=1)

			output.to_csv(outfile, index = False)





if __name__ == "__main__":
	Config = config.TestConfig()
	next = Write_ratio_dataset(Config)
	next.run()