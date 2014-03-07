import config
import pandas

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
			new_df = df.loc[:,[self.Config.keys['pct'],self.Config.keys['practice'],self.Config.keys['bnf']
			                  ,self.Config.keys['items'],self.Config.keys['quantity']
			                  ,self.Config.keys['nic']]]
			na_joined = pandas.merge(naproxen,new_df,
				left_on='BNFCODE',
				right_on=self.Config.keys["bnf"],
				how="left",
				sort=False)
			na_joined = na_joined.drop("BNFCODE",1)
			na_joined = na_joined.drop("INCLUDE",1)
			dic_joined = pandas.merge(diclofenac,new_df,
				left_on="BNFCODE",
				right_on=self.Config.keys["bnf"],
				how="left",
				sort=False)
			dic_joined = dic_joined.drop("BNFCODE",1)
			dic_joined= dic_joined.drop("INCLUDE",1)
			na_joined.to_csv(na_outfile,index=False)
			dic_joined.to_csv(dic_outfile,index=False)

if __name__ == "__main__":
	Config = config.Config()
	next = NSAID_Initial_ingest(Config)
	next.run()

