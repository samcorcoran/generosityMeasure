
# Create a dictionary of username keys and generosity values
def calculateGenerosities(tLog):
	currentPoints = dict()
	generosities = dict()
	tAmountHistory = dict()
	tPairCountHistory = dict()
	tSoloCountHistory = dict()
	for t in tLog:
		sender = t["from"]
		recipient = t["to"]

		# Validate transaction, wangbot is given exception
		if not sender == 'wangbot' and currentPoints[sender] < t["amount"]:
			continue

		# If this was a transaction between non-wangbot users, calculate generosity and update histories
		if not sender == 'wangbot' and not recipient == 'wangbot':
			# Add new users to those known
			if not sender in currentPoints:
				currentPoints[sender] = 0
			if not sender in generosities:
				generosities[sender] = 0
			if not recipient in currentPoints:
				currentPoints[recipient] = 0
			if not recipient in generosities:
				generosities[recipient] = 0

			economySize = sum(currentPoints.values())
			totalUsers = len(currentPoints)
			generosity = calculateTransactionGenerosity(t, currentPoints, economySize, totalUsers, tAmountHistory, tPairCountHistory, tSoloCountHistory, generosities)

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
				# Update information about user points

		# Remove points from sender, unless is wangbot
		if not sender == 'wangbot':
			if not sender in currentPoints:
				currentPoints[sender] = 0
			currentPoints[sender] -= t["amount"]
		# Grant points to recipient, unless is wangbot
		if not recipient == 'wangbot':
			if not recipient in currentPoints:
				currentPoints[recipient] = 0
			currentPoints[recipient] += t["amount"]

	return generosities

def calculateTransactionGenerosity(t, currentPoints, economySize, totalUsers, tAmountHistory, tPairCountHistory, tSoloCountHistory, generosities, charityWeight=1, diversityWeight=10, rGenWeight=3, dRecipWeight=6, iRecipWeight=3):
	sender = t["from"]
	recipient = t["to"]

	# Magnitude
	tMag = t["amount"]/float(currentPoints[sender])

	# Charity
	charityWeight = 1
	charityScore = 1 - min( (currentPoints[recipient] / float( (economySize/float(totalUsers)) )), 1)

	# Diversity
	diversityWeight = 10
	diversityScore = 1 - calcFavouritism(sender, recipient, tAmountHistory, tPairCountHistory, tSoloCountHistory, totalUsers)

	# Recipient Generosity
	rGenWeight = 3
	avgUserGenerosity, totalGenerosity = calcAverageGenerosity(generosities)
	rGenScore = 0.5
	if totalGenerosity > 0 and recipient in generosities:
		rGenScore = 0.5 + (0.5 * float((generosities[recipient]-avgUserGenerosity)/float(totalGenerosity)))

	# Direct Reciprocity ('to' and 'from' are switched for favouritism calculation)
	dRecipWeight = 6
	dRecipScore = 1 - calcFavouritism(recipient, sender, tAmountHistory, tPairCountHistory, tSoloCountHistory, totalUsers)

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
