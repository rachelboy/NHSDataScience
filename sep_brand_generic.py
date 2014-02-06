import pandas
import os
import config

def isGeneric(bnf):
	end_bnf = bnf[-4:] 
	return end_bnf[0:2] == end_bnf[2:4]

def sep_bran_generic(Config):
	Config.config_sep_brand_generic()
	for infile, outfile_brand, outfile_gen in Config.filenames:
		try:
			df = pandas.read_csv(infile)
		except:
			print "file", infile, "not found in", Config.data_directory
			continue

		for index,row in df.iterrows():
			bnf = row[Config.keys['bnf']]
			end_bnf = bnf[-4:] 
			if end_bnf[0:2] == end_bnf[2:4]:
				try:
					generic = generic.append(row)
				except NameError:
				 	generic = pandas.DataFrame(row)
			else:
				try:
					brand = brand.append(row)
				except NameError:
				 	brand = pandas.DataFrame(row)
		print 'to csv'
		generic.to_csv(outfile_gen,index=False)
		brand.to_csv(outfile_brand,index=False)


if __name__ == "__main__":
	Config = config.Config() #changes directory to data_directory in config
	sep_bran_generic(Config)