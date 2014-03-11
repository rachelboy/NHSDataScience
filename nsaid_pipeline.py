import config
import pandas
import util
from matplotlib import pyplot as plt
import numpy 
import matplotlib
import time

class NSAID_Pipeline(object):
	def __init__(self,Config):
		self.Config = Config


	def loadDF(self,filename):
		print "Loading", filename
		try:
			return pandas.read_csv(filename)
		except:
			print "trouble loading", filename, "in", self.Config.data_directory
			return False

class NSAID_Initial_ingest(NSAID_Pipeline):
	def run(self):
		naproxen = self.loadDF(self.Config.naproxen_file)
		diclofenac = self.loadDF(self.Config.diclofenac_file)

		naproxen = naproxen[naproxen['INCLUDE']==1]
		diclofenac = diclofenac[diclofenac['INCLUDE']==1]

		

		'''Pull out only the columns we want from the data files
		   specified in Config'''

		infiles = self.Config.append_dir("Ingest_in", group='NSAID')
		na_outfiles = self.Config.append_dir("Ingest_out_nap", group = 'NSAID')
		dic_outfiles = self.Config.append_dir("Ingest_out_dic", group = 'NSAID')
	
		for (infile, na_outfile, dic_outfile) in zip(infiles,na_outfiles, dic_outfiles):
			df = self.loadDF(infile)
			if df.empty:
				continue
			drop = ["BNFCODE","INCLUDE", self.Config.keys['quantity'],"DOSE_SCHEDULE"]
			new_df = df.loc[:,[self.Config.keys['pct'],self.Config.keys['practice'],self.Config.keys['bnf']
			                  ,self.Config.keys['quantity']]]
			na_joined = pandas.merge(naproxen,new_df,
				left_on='BNFCODE',
				right_on=self.Config.keys["bnf"],
				how="left",
				sort=False)
			
			na_joined['days_prescribed'] = na_joined[self.Config.keys['quantity']]/na_joined["DOSE_SCHEDULE"]
			na_joined = na_joined.drop(drop,axis=1)
		
			dic_joined = pandas.merge(diclofenac,new_df,
				left_on="BNFCODE",
				right_on=self.Config.keys["bnf"],
				how="left",
				sort=False)
			
			dic_joined['days_prescribed'] = dic_joined[self.Config.keys['quantity']]/dic_joined["DOSE_SCHEDULE"]
			dic_joined = dic_joined.drop(drop,axis=1)
			
			na_joined.to_csv(na_outfile,index=False)
			dic_joined.to_csv(dic_outfile,index=False)

class Sum_by_practice(NSAID_Pipeline):
	def run(self):
		na_infiles = self.Config.append_dir("Sum_by_practice_in_nap", group='NSAID')
		dic_infiles = self.Config.append_dir("Sum_by_practice_in_dic", group = 'NSAID')
		outfiles = self.Config.append_dir("Sum_by_practice_out", group = 'NSAID')
	

		for (na_infile, dic_infile, outfile) in zip(na_infiles,dic_infiles, outfiles):
			na_df = self.loadDF(na_infile)
			dic_df = self.loadDF(dic_infile)

			grouped_na = util.sumBy(na_df,[self.Config.keys['practice'], self.Config.keys['pct']])
			grouped_dic = util.sumBy(dic_df,[self.Config.keys['practice'], self.Config.keys['pct']])
			
			output = pandas.DataFrame.merge(
				grouped_na, 
				grouped_dic, 
				on=[self.Config.keys['practice'], self.Config.keys['pct']],
				how = 'outer', 
				suffixes =('_naproxen','_diclofenac'))
			print output


			output.to_csv(outfile, index = False)
class Plot(NSAID_Pipeline):
	def run_by_practice(self):
		dics = self.calc_drug_over_time()
		self.graph_drugs_line(dics)
	def run_by_PCT(self):
		dics = self.calc_drug_over_time(grouping = 'PCT')
		self.graph_drugs_line(dics, grouping = 'PCT')

	def calc_drug_over_time(self, grouping = 'practice'):
		folder = 'NSAIDSummed'
		infiles = self.Config.append_dir(folder)

		naproxen = {}
		diclofenac = {}

		for month in infiles:
			df = self.loadDF(month)
			if grouping == 'PCT':
				df = util.sumBy(df,self.Config.keys['pct'])
				time.sleep(20)
			month = month[-11:-4]

			for index,row in df.iterrows():

				if grouping == 'PCT':
					item =row[self.Config.keys['pct']]
				else:
					item = row[self.Config.keys['practice']]

				if item in naproxen.keys():
					naproxen[item][month] = row['days_prescribed_naproxen']
					diclofenac[item][month] = row['days_prescribed_diclofenac']
				else:
					naproxen[item] = {}
					naproxen[item][month] = (row['days_prescribed_naproxen'])
					
					diclofenac[item] = {}
					diclofenac[item][month] = (row['days_prescribed_diclofenac'])

		return naproxen,diclofenac

	def graph_drugs_line(self,dics, grouping = 'practice'):
		naproxen,diclofenac = dics

		months = self.Config.filenames
		months = [x.strip('.csv') for x in months]
		months.reverse()

		for practice in naproxen.keys():
			allnaproxen = []
			alldiclofenac=[]
			for month in months:
				try:
					allnaproxen.append(naproxen[practice][month])
					alldiclofenac.append(diclofenac[practice][month])
				except KeyError:
					print practice + ' not all information available'				
					break
			else:				
			 
				
				index = numpy.arange(len(months))
				#plt.subplot(2, 1, 1)
				graph = plt.plot(index, allnaproxen, 'r.-', index, alldiclofenac, 'g.-')
				
				lessMonths = [months[int(i)] for i in numpy.linspace(0,len(months)-1,num=6)]
				ax = plt.gca()
				plt.locator_params(nbins=len(lessMonths))
				ax.set_xticklabels(lessMonths)
				
				ax.set_ylabel('Sum')
				ax.set_title('Sum of naproxen and diclofenac for '+grouping+': '+practice)


				ax.legend( ('naproxen', 'diclofenac') )



				# plt.bar(range(len(quantity[drug])), quantity[drug].values(), align='center')
				# plt.xticks(range(len(quantity[drug])), quantity[drug].keys())



				
				# plt.subplot(2, 1, 2)

				# graph = plt.plot(index, costs, 'b.-')
				# ax = plt.gca()
				# plt.locator_params(nbins=len(lessMonths))
				# ax.set_xticklabels(lessMonths)
				
				# ax.set_ylabel('Sum')
				# ax.set_title('Cost (sum nic/sum quanitity) for bnf code: '+drug)




				# plt.bar(range(len(quantity[drug])), quantity[drug].values(), align='center')
				# plt.xticks(range(len(quantity[drug])), quantity[drug].keys())


				plt.show()
				# plt.savefig('Time_series_figures_generic/' + drug)
				# plt.clf()



	

if __name__ == "__main__":
	Config = config.Config()
	# next = NSAID_Initial_ingest(Config)
	# next.run()
	# next = Sum_by_practice(Config)
	# next.run()
	next = Plot(Config)
	next.run_by_practice()

