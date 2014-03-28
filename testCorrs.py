import config
import pandas
import thinkstats as ts
import util
import random


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
				ys = data[self.Config.keys['quantity']]
				corr = ts.SpearmanCorr(xs,ys)
				pVal = self.PValue(xs,ys,actual = corr)
				R2, inter, slope = self.findR2(xs,ys)

				out[folder+"_Scorr"] = out.get(folder+"_Scorr",[]) + [corr]
				out[folder+"_p"] = out.get(folder+"_p",[]) + [pVal]
				out[folder+"_R2"] = out.get(folder+"_R2",[]) + [R2]
				out[folder+"_inter"] = out.get(folder+"_inter",[]) + [inter]
				out[folder+"_slope"] = out.get(folder+"_slope",[]) + [slope]



		index=[name[0:-4] for name in self.Config.filenames]
		data = pandas.DataFrame(out,index = index)
		data.to_csv('Results/CostQuanCorrs_PPI.csv')

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
				ys = ys +data[self.Config.keys['quantity']]
			corr = ts.SpearmanCorr(xs,ys)
			pVal = self.PValue(xs,ys,actual = corr, n=1000)
			R2, inter, slope = self.findR2(xs,ys)

			out["Scorr"] = out.get("Scorr",[]) + [corr]
			out["p"] = out.get("p",[]) + [pVal]
			out["R2"] = out.get("R2",[]) + [R2]
			out["inter"] = out.get("inter",[]) + [inter]
			out["slope"] = out.get("slope",[]) + [slope]

		data = pandas.DataFrame(out,index = infolders)
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

	def findR2(self, xs, ys):

	    inter = ts.Mean(ys)
	    slope = 0
	    fxs, fys = ts.FitLine(xs, inter, slope)
	    res = ts.Residuals(xs, ys, inter, slope)
	    inter, slope = ts.LeastSquares(xs, ys)
	    res = ts.Residuals(xs, ys, inter, slope)
	    R2 = ts.CoefDetermination(ys, res)
	    return R2, inter, slope



if __name__ == "__main__":
	Config = config.Config()
	next = Find_corrs(Config)
	next.runAllTime()

