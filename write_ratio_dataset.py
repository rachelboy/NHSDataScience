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
			quantity = self.Config.keys['quantity']
			nic = self.Config.keys['nic']
			output['ratioitems']= output[items+'brand']/output[items+'generic']
			output['ratioquantity'] = output[quantity+'brand']/output[quantity+'generic']
			output['rationic'] = output[nic+'brand']/output[nic+'generic']
			

			output = output.drop(items+'brand', axis = 1)
			output = output.drop(items+'generic',axis = 1)
			output = output.drop(quantity+'brand', axis = 1)
			output = output.drop(quantity+'generic', axis = 1)
			output = output.drop(nic+'brand', axis = 1)
			output = output.drop(nic+'generic', axis = 1)
			output = output.drop('INCLUDE'+'generic', axis = 1)
			output = output.drop('GENERIC'+'generic', axis = 1)
			output = output.drop('INCLUDE'+'brand', axis = 1)
			output = output.drop('GENERIC'+'brand', axis = 1)

			output.to_csv(outfile, index = False)





if __name__ == "__main__":
	Config = config.Config()
	next = Write_ratio_dataset(Config)
	next.run()