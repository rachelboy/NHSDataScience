import pandas
import os
import config

def sep_bran_generic(Config):
	print 'in function'
	Config.config_sep_brand_generic()
	for infile, outfile_brand, outfile_gen in Config.filenames:
		try:
			print 'bringing in file'
			df = pandas.read_csv(infile)
			print 'intake file'
		except:
			print "file", infile, "not found in", Config.data_directory
			continue

		for index,row in df.iterrows():
			bnf = row[Config.keys['bnf']]
			end_bnf = bnf[-4:] 
			if end_bnf[0:2] == end_bnf[2:4]:
				print 'in if statement'
				try:
					generic.append(row)
				except:
				 	generic = Dataframe(row)
			else:
				print 'in else statement'
				try:
					brand.append(row)
				except:
				 	brand = Dataframe(row)
		print 'to csv'
		generic.to_csv(outfile_gen,index=False)
		brand.to_csv(outfile_brand,index=False)


if __name__ == "__main__":
	Config = config.Config() #changes directory to data_directory in config
	sep_bran_generic(Config)