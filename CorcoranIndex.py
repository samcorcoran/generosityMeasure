
# Create a dictionary of username keys and generosity values
def calculateGenerosities(tLog):
	print("Calculating generosities")
	generosities = dict()
	tAmountHistory = dict()
	tPairCountHistory = dict()
	tSoloCountHistory = dict()
	for t in tLog:
		print("NEXT TRANSACTION")
		print(t)
		generosity = calculateTransactionGenerosity(t, tAmountHistory, tPairCountHistory, tSoloCountHistory, generosities)
		print("Generosity: " + str(generosity))

		sender = t["from"]
		recipient = t["to"]

		# Add generosity to existing user entry
		if sender in generosities:			
			generosities[sender] += generosity
		# Or add new user to dictionary
		else:
			generosities[sender] = generosity

		# Update transaction amount histories
		if not sender in tAmountHistory:
			# Add new sender to history dict
			tAmountHistory[sender] = dict()
		# Add new recipient to dictionary, with list containing an entry for total transaction value and count
		if not recipient in tAmountHistory[sender]:
			tAmountHistory[sender][recipient] = 0
		# Increase total amount sent and transaction counter
		tAmountHistory[sender][recipient] += t["amount"]

		# Update paired transaction counts
		key = (sender, recipient)
		# Add new sender to history dict
		if not key in tPairCountHistory:
			tPairCountHistory[key] = 1
		# Or increment an existing counter
		else:
			tPairCountHistory[key] += 1

		# Update solo transaction counts
		# Add new sender to dict
		key = sender
		if not sender in tSoloCountHistory:
			tSoloCountHistory[key] = 1
		# Or increment an existing counter
		else:
			tSoloCountHistory[key] += 1
	return generosities

def calculateTransactionGenerosity(t, tAmountHistory, tPairCountHistory, tSoloCountHistory, generosities, charityWeight=1, diversityWeight=10, rGenWeight=3, dRecipWeight=6, iRecipWeight=3):
	# Magnitude
	tMag = t["amount"]/float(t["fromPoints"])
	print("tMag: " + str(tMag))

	# Charity
	charityWeight = 1
	charityScore = 1 - min( (t["toPoints"] / float( (t["economySize"]/float(t["totalUsers"])) )), 1)
	print("Charity score: " + str(charityScore))

	# Diversity
	diversityWeight = 10
	diversityScore = 1 - calcFavouritism(t["from"], t["to"], tAmountHistory, tPairCountHistory, tSoloCountHistory, t["totalUsers"])
	print("Diversity score: " + str(diversityScore))

	# Recipient Generosity
	rGenWeight = 3
	avgUserGenerosity, totalGenerosity = calcAverageGenerosity(generosities)
	rGenScore = 0.5
	if totalGenerosity > 0 and t["to"] in generosities:
		rGenScore = 0.5 + (0.5 * float((generosities[t["to"]]-avgUserGenerosity)/float(totalGenerosity)))
	print("rGen score: " + str(rGenScore))

	# Direct Reciprocity ('to' and 'from' are switched for favouritism calculation)
	dRecipWeight = 6
	dRecipScore = 1 - calcFavouritism(t["to"], t["from"], tAmountHistory, tPairCountHistory, tSoloCountHistory, t["totalUsers"])
	print("dRecipScore: " + str(dRecipScore))

	# NOTE: This was not implemented as it may simply replicate considerations of recipient generosity
	# Indirect Reciprocity
	# iRecipWeight = 3
	# iRecipScore = 1 - calcAllMutualFavourings(t["to"], t["from"])

	sumOfWeights = charityWeight + diversityWeight + rGenWeight + dRecipWeight# + iRecipWeight
	generosity = 0
	if sumOfWeights > 0:
		# Combine components
		generosity = tMag * float(
								(
									charityWeight*charityScore + 
									diversityWeight*diversityScore + 
									rGenWeight*rGenScore + 
									dRecipWeight*dRecipScore #+
									#iRecipWeight*iRecipScore
								) 
								/ 
								sumOfWeights
							)
	return generosity

def calcFavouritism(sender, recipient, tAmountHistory, tPairCountHistory, tSoloCountHistory, totalPotentialRecipients):
	# Find number of transactions from sender to recipient
	transactionsToRecipient = 0
	key = (sender, recipient)
	if key in tPairCountHistory:
		transactionsToRecipient = tPairCountHistory[key]

	# Find number of transactions from sender to anyone
	totalTransactions = 0
	if sender in tSoloCountHistory:
		totalTransactions = tSoloCountHistory[sender]

	fav = 0
	if totalTransactions > 0:
		avgTransactionsPerRecipient = totalTransactions/float(totalPotentialRecipients)
		differenceFromAvg = transactionsToRecipient - avgTransactionsPerRecipient
		fav = 0.5 + (0.5 * (differenceFromAvg/float(totalTransactions)))
	return fav

def calcAverageGenerosity(generosities):
	if generosities:
		totalGenerosity = sum(generosities.values())
		return totalGenerosity/float(len(generosities)), totalGenerosity
	return 0, 0
