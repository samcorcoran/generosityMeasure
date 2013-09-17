
# Create a dictionary of username keys and generosity values
def calculateGenerosities(tLog):
	print("Calculating generosities")
	generosities = dict()
	tAmountHistory = dict()
	tPairCountHistory = dict()
	tSoloCountHistory = dict()
	for t in tLog:
		generosity = calculateTransactionGenerosity(t, tAmountHistory, tPairCountHistory, tSoloCountHistory)

		# Add generosity to existing user entry
		if t["from"] in generosities:			
			generosities[t["from"]] += generosity
		# Or add new user to dictionary
		else:
			generosities[t["from"]] = generosity

		# Update transaction amount histories
		if not t["from"] in tAmountHistory:
			# Add new sender to history dict
			tAmountHistory[t["from"]] = dict()
		# Add new recipient to dictionary, with list containing an entry for total transaction value and count
		if not t["to"] in tAmountHistory[t["from"]]:
			tAmountHistory["from"]["to"] = 0
		# Increase total amount sent and transaction counter
		tAmountHistory["from"]["to"][0] += amount

		# Update paired transaction counts
		key = (t["from"], t["to"])
		# Add new sender to history dict
		if not key in tPairCountHistory:
			tPairCountHistory[key] = 1
		# Or increment an existing counter
		else:
			tPairCountHistory[key] += 1

		# Update solo transaction counts
		# Add new sender to dict
		if not t["from"] in tSoloCountHistory:
			tSoloCountHistory[t["from"]] = 1
		# Or increment an existing counter
		else:
			tSoloCountHistory[t["from"]] += 1
	return generosities

def calculateTransactionGenerosity(t, tAmountHistory, tPairCountHistory, tSoloCountHistory, charityWeight=1, diversityWeight=10, rGenWeight=3, dRecipWeight=6, iRecipWeight=3):
	# Magnitude
	tMag = t["amount"]/t["fromPoints"]

	# Charity
	charityWeight = 1
	charityScore = 1 - min( (t["toPoints"] / (t["economySize"]/t["totalUsers"])), 1)

	# Diversity
	diversityWeight = 10
	diversityScore = 1 - calcFavouritism(t["from"], t["to"], tAmountHistory, tPairCountHistory, tSoloCountHistory, t["totalUsers"])

	# Recipient Generosity
	rGenWeight = 3
	avgUserGenerosity, totalGenerosity = calcAverageGenerosity()
	rGenScore = 0
	if totalGenerosity > 0:
		rGenScore = 0.5 + (0.5 * ((t.recipient.generosity-avgUserGenerosity)/totalGenerosity))

	# Direct Reciprocity
	dRecipWeight = 6
	dRecipScore = 1 - calcFavouritism(t.recipient, t.sender)

	# Indirect Reciprocity
	iRecipWeight = 3
	iRecipScore = 1 - calcAllMutualFavourings(t.recipient, t.sender)

	sumOfWeights = charityWeight + diversityWeight + rGenWeight + dRecipWeight + iRecipWeight
	generosity = 0
	if sumOfWeights > 0:
		# Combine components
		generosity = tMag * (
								(charityWeight*charityScore + 
								diversityWeight*diversityScore + 
								rGenWeight*rGenScore + 
								dRecipWeight*dRecipScore +
								iRecipWeight*iRecipScore) 
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
		avgTransactionsPerRecipient = totalTransactions/totalPotentialRecipients
		differenceFromAvg = transactionsToRecipient - avgTransactionsPerRecipient
		fav = 0.5 + (0.5 * (differenceFromAvg/totalTransactions))
	return fav
