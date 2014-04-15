import config
import pandas
import util
from matplotlib import pyplot as pp
import numpy 
import matplotlib
import time
import numpy as np

class Psych_Pipeline(object):
	def __init__(self,Config):
		self.Config = Config
		self.psychdata = self.loadDF(self.Config.psych_file)
		if self.psychdata.empty:
			print 'antipsychotics chem code file missing'


	def loadDF(self,filename):
		print "Loading", filename
		try:
			return pandas.read_csv(filename)
		except:
			print "trouble loading", filename, "in", self.Config.data_directory
			return False

	def run(self):
		for infile, outfile in zip(self.infiles,self.outfiles):
			df = self.loadDF(infile)
			if df.empty:
				continue

			out = self.process(df)

			out.to_csv(outfile, index=False)

class Psych_Initial_Ingest(Psych_Pipeline):
	def __init__(self,Config):
		super(Psych_Initial_Ingest,self).__init__(Config)
		self.infiles = self.Config.append_dir('Ingest_in',group = 'psych')
		self.outfiles = self.Config.append_dir('Ingest_out',group = 'psych')

	def process(self,df):
		df = df.loc[:,[self.Config.keys['ccg'],self.Config.keys['pct'],self.Config.keys['practice']
								,self.Config.keys['bnf'],self.Config.keys['quantity'],self.Config.keys['items']]]
		df['chem code'] = df[self.Config.keys['bnf']].apply(lambda x: x[:9])
		df['generic'] = df[self.Config.keys['bnf']].map(lambda x: 1 if str(x)[-4:-2] == str(x)[-2:] else 0)
			
		out = pandas.merge(self.psychdata,df,
			on = 'chem code',
			how="left",
			sort=False)

		return out.drop('Unnamed: 2')


class Sum_Chem_Gen(Psych_Pipeline):
	def __init__(self,Config):
		super(Sum_Chem_Gen,self).__init__(Config)
		self.infiles = self.Config.append_dir('Ingest_out',group = 'psych')
		self.outfiles = self.Config.append_dir('Summed_Chem_Gen',group = 'psych')

	def process(self,df):
		return util.sumBy(df,['chem code','name','CCG','PCT','generic'])




def sumLists(l1,l2):
	return [x+y for x,y in zip(l1,l2)]

def stackPlot(Config):
	infiles = Config.append_dir("Ingest_out", group='psych')
	antipsych = pandas.read_csv('Criteria/antipsychotics.csv',index_col='chem code')

	data = {}
	for i,r in antipsych.iterrows():
		data[r['name']] = []

	for infile in infiles:
		print "Loading", infile
		df = pandas.read_csv(infile)

		df = util.sumBy(df,['chem code','name'])
		df = df.set_index('chem code')
		for i,r in antipsych.iterrows():
			try:
				#relies on chem code being index
				tot = df.loc[i][Config.keys['items']]
			except KeyError:
				tot = 0
			if tot != tot:
				tot = 0
			data[r['name']].append(tot)

	prev = None
	lines = []
	legends = []
	for key, value in sorted(data.items(),key=lambda x : numpy.mean(x[1])):
		if prev:
			prev = sumLists(prev,value)
		else:
			prev = value
		if numpy.mean(value) < 1000:
			pp.plot(prev)
		else:
			lines = pp.plot(prev) + lines
			legends = [key] + legends

	pp.legend(lines,legends)
	pp.title('Cumulative presecriptions of antipsychotics')
	pp.ylabel('# prescriptions')
	pp.xlabel('months since Jan 2012')
	pp.show()

def chemGenBrandComp(Config):
	infiles = Config.append_dir("Summed_Chem_Gen", group='psych')
	antipsych = pandas.read_csv('Criteria/antipsychotics.csv',index_col='chem code')

	data = {}
	for i,r in antipsych.iterrows():
		data[r['name']] = {'brand':[0 for i in range(len(infiles))],
			'gen':[0 for i in range(len(infiles))]}

	mon = 0
	for infile in infiles:
		print "Loading", infile
		df = pandas.read_csv(infile,index_col = False)

		df = util.sumBy(df,['chem code','name','generic'])
		for i,r in df.iterrows():
			if r['generic'] == 1:
				gen = 'gen'
			else:
				gen = 'brand'
			tot = r[Config.keys['items']]
			data[r['name']][gen][mon] = tot

		mon += 1

	for key, value in data.items():
		if np.sum(value['brand'])>0 or np.sum(value['gen'])>0:
			pp.plot(value['brand'],'r*-',label = 'brand')
			pp.plot(value['gen'],'bo-',label = 'generic')

			pp.legend()
			pp.title('Total prescriptions of '+key)
			pp.ylabel('# prescriptions')
			pp.xlabel('months since Jan 2012')
			pp.show()

if __name__ == "__main__":
	Config = config.Config()
	# next = Psych_Initial_Ingest(Config)
	# next.run()
	# next = Sum_Chem_Gen(Config)
	# next.run()
	# stackPlot(Config)
	chemGenBrandComp(Config)