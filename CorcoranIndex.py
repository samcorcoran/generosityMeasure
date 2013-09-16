import math

# Create a dictionary of username keys and generosity values
def calculateGenerosities(tLog):
	print("Calculating generosities")
	generosities = dict()
	for t in tLog:
		generosity = 0
		# Add generosity to existing user entry
		if t["from"] in generosities:			
			generosities[t["from"]] += generosity
		# Add new user to dictionary
		else:
			generosities[t["from"]] = generosity
	return generosities
