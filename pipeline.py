import config
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

class Initial_ingest(Pipeline):

	def run(self):
		'''Pull out only the columns we want from the data files
		   specified in Config'''

		infiles = self.Config.append_dir("Ingest_in")
		outfiles = self.Config.append_dir("Ingest_out")

		for (infile, outfile) in zip(infiles,outfiles):
			df = self.loadDF(infile)
			if not df:
				continue
			new_df = df.loc[:,[self.Config.keys['practice'],self.Config.keys['bnf']
			                  ,self.Config.keys['items'],self.Config.keys['quantity']
			                  ,self.Config.keys['nic']]]
			new_df.to_csv(outfile,index=False)

class Join_ppis(Pipeline):

	def run(self):
		'''attach post codes for each practice'''

		try:
			ppis = pandas.read_csv(self.Config.ppis_file)
		except:
			print "trouble loading", self.Config.ppis_file, "in", self.Config.data_directory
			return

		datafiles = self.Config.append_dir("Join_ppis_in")
		outfiles = self.Config.append_dir("Join_ppis_out")

		for (datafile, outfile) in zip(datafiles,outfiles):
			rxs = self.loadDF(datafile)
			if not rxs:
				continue

			include = ppis.loc[:,["BNFCODE","INCLUDE","GENERIC"]]

			joined = pandas.merge(rxs,include,
				left_on=self.Config.keys["bnf"],
				right_on="BNFCODE",
				sort=False)
			joined = joined.drop("BNFCODE",1)
			selected = joined[joined['INCLUDE']==1]

			selected.to_csv(outfile,index=False)

			# df['DRUG TYPE'] = df.apply(lambda row: 
			# 	'Generic' if self.isGeneric(row[self.Config.keys['bnf']]) else 'Brand'
			# 	,axis=1)

			# grouped = df.groupby('DRUG TYPE')
			# grouped.get_group('Brand').to_csv(outfile_brand,index=False)
			# grouped.get_group('Generic').to_csv(outfile_gen,index=False)

class Join_post_codes(Pipeline):


	def run(self):
		'''attach post codes for each practice'''
		
		datafiles = self.Config.append_dir("Join_post_codes_in")
		outfiles = self.Config.append_dir("Join_post_codes_out")
		addsfiles = self.Config.append_dir("Addresses")

		for (datafile,outfile,addsfile) in zip(datafiles, outfiles, addsfiles):
			try:
				addresses = pandas.read_csv(addsfile,
					header = 0,
					names=["month","practice","name","parent org","street",
					"town","county",self.Config.keys['post code']])
			except:
				print "trouble loading", addsfile, "in", self.Config.data_directory
				return
			rxs = self.loadDF(datafile)
			if rxs.empty:
				continue

			postCodes = addresses.loc[:,["practice",self.Config.keys['post code']]]
			joined = pandas.merge(rxs,postCodes,
				left_on=self.Config.keys["practice"],
				right_on="practice",
				how="left",
				sort=False)
			joined = joined.drop("practice",1)
			joined.to_csv(outfile,index=False)


class Sep_brand_generic(Pipeline):

	def run(self):
		'''put branded and generic drugs in separate files'''

		infiles = self.Config.append_dir('Sep_brand_generic_in')
		outfiles_brand = self.Config.append_dir('Sep_brand_out')
		outfiles_gen = self.Config.append_dir('Sep_generic_out')

		for (infile, outfile_brand, outfile_gen) in zip(infiles,outfiles_brand,outfiles_gen):
			df = self.loadDF(infile)
			if df.empty:
				continue

			# df['DRUG TYPE'] = df.apply(lambda row: 
			# 	'Generic' if self.isGeneric(row[self.Config.keys['bnf']]) else 'Brand'
			# 	,axis=1)

			df[df['GENERIC']==0].to_csv(outfile_brand,index=False)
			df[df['GENERIC']==1].to_csv(outfile_gen,index=False)
class Map_prep(Pipeline):
	def run(self):
		'''create dataset to use for mapping, one for PCT and one for CCG accross all months'''
		infiles = self.Config.append_dir('Map_prep_in')
		ratios = {}

		branditemsccg = {}
		genericitemsccg = {}
		branditemspct = {}
		genericitemspct = {}
		for infile in infiles:
			df =  self.loadDF(infile)
			df['branditems'] = df['sumitems']*df['percitems']
			df['genericitems'] = df['sumitems']-df['branditems']
			drop = list(df.columns.values)
			drop.remove('CCG')
			drop.remove('PCT')
			drop.remove('branditems')
			drop.remove('genericitems')
			df = df.drop(drop,1)
			
			if infile[-11:] in self.Config.before_ccgs:
				# groupedbrand = util.sumBy(branddf,[self.Config.keys['pct']])
				# groupedgeneric = util.sumBy(genericdf,[self.Config.keys['pct']])
				for row_index, row in df.iterrows():
					# if row[1] in branditemspct.keys():
					
						branditemspct[row[1]] = branditemspct.get(row[1],0) + row[2]
						genericitemspct[row[1]] = genericitemspct.get(row[1],0) + row[3]
					# else:
					# 	branditemspct[row[1]] = row[2]
					# 	genericitemspct[row[1]] = row[3]	

			else:
				for row_index, row in df.iterrows():

					# if row[0] in branditemsccg.keys():
						branditemsccg[row[0]] = branditemsccg.get(row[0],0) + row[2]
						genericitemsccg[row[0]] = genericitemsccg.get(row[0],0) + row[3]
					# else:
					# 	branditemsccg[row[0]] = [row[2]]
					# 	genericitemsccg[row[0]] = [row[3]]



		ratioitemspct = {}
		ratioitemsccg = {}
		for pct in branditemspct.keys():
			sums = genericitemspct[pct] + branditemspct[pct]
			ratio = branditemspct[pct]/sums
			ratioitemspct[pct] = ratio
		for ccg in branditemsccg.keys():
			sums = genericitemsccg[ccg] + branditemsccg[ccg]
			ratio = branditemsccg[ccg]/sums
			ratioitemsccg[ccg] = ratio
		
		df_pct = pandas.DataFrame(ratioitemspct.items(), columns=['PCT','percen'])#, index = False)
		df_ccg = pandas.DataFrame(ratioitemsccg.items())#, index = False)
		print df_pct
		pct_names =  self.loadDF('Criteria/pctCodeToName.csv')
		joined = pandas.merge(df_pct,pct_names,
			left_on='PCT',
			right_on='code',
			sort=False)
		joined.to_csv('Mapping/PPISpct.csv',index=False)
		df_ccg.to_csv('Mapping/PPISccg.csv',index=False)
	# def Join_PCT_names(self):
	# 	pct_names =  self.loadDF('Mapping/PPISpct.csv')
	# 	addresses =  self.loadDF('Criteria/pctCodeToName.csv')
	# 	joined = pandas.merge(pct_names,addresses,
	# 		left_on='0',
	# 		right_on='code',
	# 		sort=False)
	# 	joined.to_csv('Mapping/PPISpct.csv',index=False)
if __name__ == "__main__":
	Config = config.Config() #changes directory to data_directory in config
	# next = Initial_ingest(Config)
	# next.run()
	# next = Join_ppis(Config)
	# next.run()
	# next = Join_post_codes(Config)
	# next.run()
	# next = Sep_brand_generic(Config)
	# next.run()
	next2 = Map_prep(Config)
	next2.run()
