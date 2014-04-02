import config
import pandas
import thinkstats as ts
import util
import random
import math
import matplotlib.pyplot as pp


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

class Find_corrs(Pipeline):
	def run(self):
		out = {}
		infolders =  self.Config.directories['CorrsIn']
		for folder in infolders:
			infiles = self.Config.append_dir(folder)
			for infile in infiles:	
				data = self.loadDF(infile)
				data = util.sumBy(data,self.Config.keys['bnf'])
				data['cost'] = data[self.Config.keys['nic']]/data[self.Config.keys['quantity']]
				data = data.to_dict(outtype = 'list')
				xs = data['cost']
				ys = data[self.Config.keys['items']]

				corr = ts.SpearmanCorr(xs,ys)
				pVal = self.PValue(xs,ys,actual = corr, n=1000)
				sdev,serr, inter, slope = self.regress(xs,ys)

				out["Month"] = out.get("Month",[]) + [infile[-11:-4]]
				out["Group"]  = out.get("Group",[]) + [folder]
				out["transform"] = out.get("transform",[]) + ['linear']
				out["Scorr"] = out.get("Scorr",[]) + [corr]
				out["p"] = out.get("p",[]) + [pVal]
				out["Stan Dev"] = out.get("Stan Dev",[]) + [sdev]
				out["Stan Err"] = out.get("Stan Err", []) + [serr]
				out["inter"] = out.get("inter",[]) + [inter]
				out["slope"] = out.get("slope",[]) + [slope]

				sdev,serr,inter,slope = self.regress(xs,ys,ylog=True)

				out["Month"] = out.get("Month",[]) + [infile[-11:-4]]
				out["Group"]  = out.get("Group",[]) + [folder]
				out["transform"] = out.get("transform",[]) + ['log']
				out["Scorr"] = out.get("Scorr",[]) + [corr]
				out["p"] = out.get("p",[]) + [pVal]
				out["Stan Dev"] = out.get("Stan Dev",[]) + [sdev]
				out["Stan Err"] = out.get("Stan Err", []) + [serr]
				out["inter"] = out.get("inter",[]) + [inter]
				out["slope"] = out.get("slope",[]) + [slope]

		data = pandas.DataFrame(out)
		data.to_csv('Results/CostQuanCorrs_PPI.csv', index=False)

	def runAllTime(self):
		out = {}
		infolders =  self.Config.directories['CorrsIn']
		
		for folder in infolders:
			infiles = self.Config.append_dir(folder)
			xs = []
			ys = []
			for infile in infiles:	
				data = self.loadDF(infile)
				data = util.sumBy(data,self.Config.keys['bnf'])
				data['cost'] = data[self.Config.keys['nic']]/data[self.Config.keys['quantity']]
				data = data.to_dict(outtype = 'list')
				xs = xs+ data['cost']
				ys = ys +data[self.Config.keys['items']]
			corr = ts.SpearmanCorr(xs,ys)
			pVal = self.PValue(xs,ys,actual = corr, n=1000)
			sdev,serr, inter, slope = self.regress(xs,ys)

			out["Group"]  = out.get("Group",[]) + [folder]
			out["transform"] = out.get("transform",[]) + ['linear']
			out["Scorr"] = out.get("Scorr",[]) + [corr]
			out["p"] = out.get("p",[]) + [pVal]
			out["Stan Dev"] = out.get("Stan Dev",[]) + [sdev]
			out["Stan Err"] = out.get("Stan Err", []) + [serr]
			out["inter"] = out.get("inter",[]) + [inter]
			out["slope"] = out.get("slope",[]) + [slope]

			sdev,serr,inter,slope = self.regress(xs,ys,ylog=True)

			out["Group"]  = out.get("Group",[]) + [folder]
			out["transform"] = out.get("transform",[]) + ['log']
			out["Scorr"] = out.get("Scorr",[]) + [corr]
			out["p"] = out.get("p",[]) + [pVal]
			out["Stan Dev"] = out.get("Stan Dev",[]) + [sdev]
			out["Stan Err"] = out.get("Stan Err", []) + [serr]
			out["inter"] = out.get("inter",[]) + [inter]
			out["slope"] = out.get("slope",[]) + [slope]

			# pp.scatter(xs,ys)
			# pp.yscale('log')
			# pp.show()

		data = pandas.DataFrame(out,index = None)
		data.to_csv('Results/CostQuanCorrs_PPI_AllTime.csv')



	def SimulateNull(self,xs, ys):
	    random.shuffle(xs)
	    random.shuffle(ys)
	    return ts.SpearmanCorr(xs, ys)


	def PValue(self,xs, ys, actual = None, n=50):
		if not actual:
			actual = ts.Corr(xs, ys)

		xs_copy = list(xs)
		ys_copy = list(ys)

		corrs = []
		for i in range(n):
			corr = self.SimulateNull(xs_copy, ys_copy)
			corrs.append(corr)

	    # what does the distribution of corrs look like?

		hits = [corr for corr in corrs if abs(corr) >= abs(actual)]
		p = len(hits) / float(n)
		return p

	def regress(self, xs, ys, ylog = False):

	    if ylog:
	    	y_t = [math.log(y) for y in ys]
	    	inter, slope = ts.LeastSquares(xs, y_t)
	    	res = ts.LogYResiduals(xs, ys, inter, slope)
	    else:
	    	inter, slope = ts.LeastSquares(xs, ys)
	    	res = ts.Residuals(xs, ys, inter, slope)
	    ybar, yvar = ts.MeanVar(ys)
	    rbar,rvar = ts.MeanVar(res)

	    return math.sqrt(yvar), math.sqrt(rvar), inter, slope

	def plotAllTime(self):
		lines = self.loadDF('Results/CostQuanCorrs_PPI_AllTime.csv')
		lines = lines.groupby('Group')
		for name, group in lines:
			xs = []
			ys = []
			for month in self.Config.filenames:
				data = self.loadDF(name+'/'+month)
				data = util.sumBy(data,self.Config.keys['bnf'])
				data['cost'] = data[Config.keys['nic']]/data[Config.keys['quantity']]
				data = data.to_dict(outtype='list')
				xs = xs + data['cost']
				ys = ys + data[self.Config.keys['items']]
			pp.scatter(xs,ys)
			fxs = [x/20.0 for x in range(30)]
			for index,row in group.iterrows():
				if row['transform'] == 'linear':
					fys = [x*row['slope']+row['inter'] for x in fxs]
					pp.plot(fxs,fys,'-.',label='linear')
				if row['transform'] == 'log':
					fys = [math.exp(x*row['slope']+row['inter']) for x in fxs]
					pp.plot(fxs,fys,'-',label='log')
			pp.legend()
			pp.title(name)
			pp.ylabel('items')
			pp.xlabel('cost')
			# pp.yscale('log')
			pp.show()

	def plotRegression(self):
		lines = self.loadDF('Results/CostQuanCorrs_PPI.csv')
		lines = lines.groupby('Group')
		for name, group in lines:
			group = group.groupby('Month')
			for month, fits in group:
				data = self.loadDF(name+'/'+month+'.csv')
				data = util.sumBy(data,self.Config.keys['bnf'])
				data['cost'] = data[Config.keys['nic']]/data[Config.keys['quantity']]
				data = data.to_dict(outtype='list')
				pp.scatter(data['cost'],data[self.Config.keys['items']])
				xs = [x/20.0 for x in range(30)]
				for index,row in fits.iterrows():
					if row['transform'] == 'linear':
						ys = [x*row['slope']+row['inter'] for x in xs]
						pp.plot(xs,ys,'-.',label='linear')
					if row['transform'] == 'log':
						ys = [math.exp(x*row['slope']+row['inter']) for x in xs]
						pp.plot(xs,ys,'-',label='log')
				pp.legend()
				pp.title(name+' '+month)
				pp.ylabel('items')
				pp.xlabel('cost')
				pp.yscale('log')
				pp.show()





if __name__ == "__main__":
	Config = config.Config()
	next = Find_corrs(Config)
	# next.run()
	# next.plotRegression()
	# next.runAllTime()
	next.plotAllTime()
