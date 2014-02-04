import config
import pandas
import numpy as np
import thinkstats as ts
import thinkplot as tp

def sumBy(df,key):
	return df.groupby(key).aggregate(np.sum)

def testSumBy():
	df = pandas.DataFrame.from_dict(
		{'A':['a','b','a','b','c']
		,'B':['AA','BB','CC','DD','EE']
		,'C':[1.0,2.0,3.0,4.0,5.0]
		,'D':['1.0','2.0','3.0','4.0','5,0']})
	summed = sumBy(df,'A')
	print summed

def makeDrugSums():
	Config = config.Config()
	df = pandas.read_csv("Sep2013Drug.csv")
	summed = sumBy(df,Config.keys['bnf'])
	summed.to_csv('SummedByDrug.csv')


if __name__ == "__main__":
	Config = config.Config()
	costs = pandas.read_csv("SummedByDrug.csv").to_dict(outtype='list')
	pmf = ts.MakePmfFromList(costs[Config.keys['nic']])
	cdf = pmf.MakeCdf()
	tp.Cdf(cdf)
	tp.show()

