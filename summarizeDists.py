import util
import config
import thinkplot as tp
import thinkstats as ts
import pandas

if __name__ == "__main__":
	Config = config.TestConfig()
	datafile = "CompressedData/tiny.csv"
	key = Config.keys['nic']

	df = pandas.read_csv(datafile)
	df = util.sumBy(df,Config.keys['bnf'])

	data = df.to_dict(outtype='list')
	pmf = ts.MakePmfFromList(data[key])
	cdf = pmf.MakeCdf()

	print "Mean", pmf.Mean()
	print "Median", cdf.Value(.5)
	print "Standard Deviation", (pmf.Var())**.5

	tp.SubPlot(2, 3, 1)
	tp.Pmf(pmf)
	tp.Config(title='pmf')

	tp.SubPlot(2, 3, 2)
	scale = tp.Cdf(cdf, xscale='log')
	tp.Config(title='logx', **scale)

	tp.SubPlot(2, 3, 3)
	scale = tp.Cdf(cdf, transform='exponential')
	tp.Config(title='expo', **scale)

	tp.SubPlot(2, 3, 4)
	xs, ys = ts.NormalProbability(data[key])
	tp.Plot(xs, ys)
	tp.Config(title='normal')

	tp.SubPlot(2, 3, 5)
	scale = tp.Cdf(cdf, transform='pareto')
	tp.Config(title='pareto', **scale)

	tp.SubPlot(2, 3, 6)
	scale = tp.Cdf(cdf, transform='weibull')
	tp.Config(title='weibull', **scale)

	tp.Show()