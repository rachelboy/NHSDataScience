import pandas
import config

def joinPostCodes(Config):
	Config.config_join_addresses()
	for datafile, addsfile, outfile in Config.filenames:
		try:
			rxs = pandas.read_csv(datafile)
			try:
				addresses = pandas.read_csv("addresses.csv",
					header=None, 
					names=["practice","name","parent org","street",
					"town","county","postal code"])
			except:
				print "file", infile, "not found in", Config.data_directory
				continue
		except:
			print "file", infile, "not found in", Config.data_directory
			continue
		postCodes = addresses.loc[:,["practice","postal code"]]
		joined = pandas.merge(rxs,postCodes,
			left_on=Config.keys["practice"],
			right_on="practice",
			how="left",
			sort=False)
		joined = joined.drop("practice",1)
		joined.to_csv(outfile,index=False)


if __name__=="__main__":
	Config = config.Config()
	joinPostCodes(Config)
