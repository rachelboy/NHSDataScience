import config
import thinkstats as ts
import csv
import pandas
import util

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

class SummaryStats(Pipeline):
	'''get mean, median, and standard deviation for 
	expenditures, cost, and quantity'''

	def __init__(self,Config):
		super(SummaryStats,self).__init__(Config)

		self.inDirs = self.Config.directories['Summary_stats_in']
		self.outDir = self.Config.directories['Summary_stats_out']

		self.inputs = [self.Config.append_dir(dirc) for dirc in self.inDirs]
		
		self.distFuns = [('Expenditures',self.ExpendituresDist),
						('Costs',self.CostsDist),
						('Quantity',self.QuantityDist)]

	def run(self):
		for files, dirname in zip(self.inputs,self.inDirs):
			dists = {}
			for datafile in files:
				date = datafile[-11:-4]

				df = self.loadDF(datafile)
				df = util.sumBy(df,self.Config.keys['bnf'])

				for distFun in self.distFuns:
					res = distFun[1](df)
					res['Date'] = date

					dists[distFun[0]] = dists.get(distFun[0],[]) + [res]

			for distFun in self.distFuns:
				outfile = self.outDir+'/'+dirname+'_'+distFun[0]+'_SummaryStats.csv'
				df = pandas.DataFrame(dists[distFun[0]])
				df.to_csv(outfile,index=None)

	def ExpendituresDist(self,df):
		return self.examineDist(df,Config.keys['nic'])

	def CostsDist(self,df):
		df['ITEM COST'] = df[self.Config.keys['nic']]/df[self.Config.keys['quantity']]
		return self.examineDist(df,'ITEM COST')

	def QuantityDist(self,df):
		return self.examineDist(df,self.Config.keys['quantity'])

	def examineDist(self,df,key):
		data = df.to_dict(outtype='list')
		pmf = ts.MakePmfFromList(data[key])
		cdf = pmf.MakeCdf()

		stats = self.getStats(pmf,cdf=cdf)

		return stats

	def getStats(self,pmf,cdf=None):
		if not cdf:
			cdf = pmf.MakeCdf()
		return {'Mean':pmf.Mean(), 'Median':cdf.Value(.5), 
				'StdDev': (pmf.Var())**.5}


if __name__=="__main__":
	Config = config.Config()
	next = SummaryStats(Config)
	next.run()