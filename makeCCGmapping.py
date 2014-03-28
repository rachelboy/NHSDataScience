import config
import pandas
import os.path

class Pipeline(object):
	def __init__(self,Config):
		self.Config = Config


	def loadDF(self,filename):
		print "Loading", filename
		try:
			return pandas.read_csv(filename)
		except:
			print "trouble loading", filename, "in", self.Config.data_directory
			return False

class CCG_mapping(Pipeline):
	'''make a file that maps from practices to the CCGs they occupy, 
	in order to group practices before April 2013'''

	def run(self):
		if not os.path.isfile(self.Config.CCGfile):
			self.makeMapping()

		mapping = self.loadDF(self.Config.CCGfile)
		infiles = self.Config.append_dir('PCT_to_CCG_in')
		outfiles = self.Config.append_dir('PCT_to_CCG_out')

		for infile, outfile in zip(infiles,outfiles):
			data = self.loadDF(infile)
			if infile[-11:] in self.Config.before_ccgs:
				data = pandas.merge(data,mapping,
					on = self.Config.keys['practice'],
					how = 'left',
					sort=False)
			else:
				data[self.Config.keys['ccg']] = data[self.Config.keys['pct']]
			data = data.loc[:,[self.Config.keys['practice'],self.Config.keys['bnf']
			                  ,self.Config.keys['items'],self.Config.keys['quantity']
			                  ,self.Config.keys['nic'],self.Config.keys['ccg']
			                  ,self.Config.keys['pct']]]
			data.to_csv(outfile,index=False)

	def makeMapping(self):
		aprData = self.loadDF(self.Config.directories['PCT_to_CCG_in']+'/Apr2013.csv')
		prac_CCG = pandas.DataFrame(
			{self.Config.keys['ccg']:aprData[self.Config.keys['pct']],
			 self.Config.keys['practice']:aprData[self.Config.keys['practice']]})
		prac_CCG.drop_duplicates(inplace=True)
		prac_CCG.to_csv(self.Config.CCGfile)

if __name__=="__main__":
	Config = config.Config()
	next = CCG_mapping(Config)
	next.run()