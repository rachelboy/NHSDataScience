import config
class Write_ratio_dataset(Pipeline):
	def run(self):
		bfile = self.Config.append_dir("WriteRatioDatasetBrand")
		gfile = self.Config.append_dir("WriteRatioDatasetGeneric")

		output = []
		for (brand, generic, month) in zip(bfile,gfile,self.Config.filenames):
			brandfile = self.loadDF(brand)
			genericfile = self.loadDF(generic)
			brandnum = len(brandfile.index)
			genericnum = len(genericfile.index)
			ratio = brandnum/genericnum
			output.append(month,ratio)
		output.to_csv('Generic_Brand_Ratios')





if __name__ == "__main__":
	Config = config.Config()
	write_ratio_dataset.py(Config)