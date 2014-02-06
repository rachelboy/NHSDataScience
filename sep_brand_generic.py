import pandas
import os
import config

def isGeneric(bnf):
	end_bnf = bnf[-4:] 
	return end_bnf[0:2] == end_bnf[2:4]

def sep_bran_generic(Config):
	Config.config_sep_brand_generic()
	generic = []
	brand = []
	for infile, outfile_brand, outfile_gen in Config.filenames:
		try:
			df = pandas.read_csv(infile)
			print df
		except:
			print "file", infile, "not found in", Config.data_directory
			continue

		for index,row in df.iterrows():
			bnf = row[Config.keys['bnf']]
			end_bnf = bnf[-4:] 
			if end_bnf[0:2] == end_bnf[2:4]:
				generic.append(row)
			else:
				brand.append(row)

		generic_df = pandas.DataFrame(generic)
		brand_df = pandas.DataFrame(brand)
		generic_df.to_csv(outfile_gen,index=False)
		brand_df.to_csv(outfile_brand,index=False)


if __name__ == "__main__":
	Config = config.Config() #changes directory to data_directory in config
	sep_bran_generic(Config)