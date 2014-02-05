def printVals(df,key,keyVal,cols):
	for index,row in df.iterrows():
		if row[key] == keyVal:
			print [row[col] for col in cols]