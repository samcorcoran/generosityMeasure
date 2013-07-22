import math

import Users
import Transaction

print("\nGenerosity Measure Test\t")

def createUsers():
	print("Creating some users...")
	# Create some users
	usernames = ['sam', 'mark', 'will', 'ben']
	users = []
	for name in usernames:
		users.extend([Users.User(name)])
	return users

def printAllUsers(users):
	# Print all users
	print("Printing all users...")
	for user in users:
		user.printInfo()

def totalEconomySize():
	totalPoints = 0
	for u in users:
		totalPoints += u.points
	return totalPoints

def calcFavoratism(sender, recipient):
	transactionsToRecipient = 0
	totalTransactions = 0
	totalPotentialRecipients = len(users)
	# Scan logs
	for t in transactionLog:
		if t.sender == sender:
			totalTransactions += 1
			if t.recipient == recipient:
				transactionsToRecipient += 1
	# Calculate
	fav = 0
	if totalTransactions > 0:
		avgTransactions = totalTransactions/totalPotentialRecipients
		differenceFromAvg = transactionsToRecipient - avgTransactions
		fav = 0.5 + (0.5 * (differenceFromAvg/totalTransactions))
	return fav

def calcAverageGenerosity():
	totalGenerosity = 0
	for u in users:
		totalGenerosity += u.generosity
	return totalGenerosity/len(users), totalGenerosity

def calculateMutualFavouring(userOne, userTwo):
	return calcFavoratism(userOne, userTwo) * calcFavoratism(userTwo, userOne)

def calcAllMutualFavourings(userOne, ignoredUser=False):
	mutualFavouringScore = 0
	totalComparisons = 0
	for u in users:
		if not u == userOne:
			# not self
			if not (ignoredUser and u == ignoredUser) :
				# not the ignored user
					mutualFavouringScore += calculateMutualFavouring(userOne, u)
					totalComparisons += 1					
	return mutualFavouringScore/totalComparisons

def calcTransactionGenerosity(t):
	# Magnitude
	tMag = t.amount/t.senderFundsPre
	# Charity
	charityWeight = 1
	totalUserbasePoints = totalEconomySize()
	charityScore = 1 - min( (t.recipientFundsPre/(totalUserbasePoints/len(users))), 1)

	# Diversity
	diversityWeight = 5
	diversityScore = 1 - calcFavoratism(t.sender, t.recipient)

	# Recipient Generosity
	rGenWeight = 2
	avgUserGenerosity, totalGenerosity = calcAverageGenerosity()
	rGenScore = 0
	if totalGenerosity > 0:
		rGenScore = 0.5 + (0.5 * ((t.recipient.generosity-avgUserGenerosity)/totalGenerosity))

	# Direct Reciprocity
	dRecipWeight = 3
	dRecipScore = 1 - calcFavoratism(t.recipient, t.sender)

	# Indirect Reciprocity
	iRecipWeight = 2
	iRecipScore = 1 - calcAllMutualFavourings(t.recipient, t.sender)

	# Combine components
	generosity = tMag * (
							(charityWeight*charityScore + 
							diversityWeight*diversityScore + 
							rGenWeight*rGenScore + 
							dRecipWeight*dRecipScore +
							iRecipWeight*iRecipScore) 
							/ 
							(charityWeight + 
							diversityWeight +
							rGenWeight +
							dRecipWeight +
							iRecipWeight)
						)
	return generosity

def transfer(sender, recipient, points):
	# Restrict to integer transfers
	if not isinstance(points, int):
		return False
	# validate amount
	if not (points > 0 or points <= sender.points):
		return False
	# Create transaction
	transaction = Transaction.Transaction(sender, recipient, points)
	# Generosity
	generosity = calcTransactionGenerosity(transaction)
	# send funds
	if not transaction.executed:
		transaction.execute()
	transactionLog.extend([transaction])
	return transaction

def performBasicTransactions(users):
	print("Simulating some basic transactions...")
	# Simulate some trading
	totalUsers = len(users)
	for i in range(0,totalUsers):
		# Give previous user 5
		transfer(users[i], users[i-1], 5)
		# Give next user 2
		transfer(users[i], users[i-(totalUsers-1)], 2)

def performUnevenTransactions(users):
	print("Performing uneven transactions...")
	# 0 gives 1 10%
	transfer(users[0], users[1], 3)
	# 3 gives 0 20%, 3 gives 2 10%
	transfer(users[3], users[0], 2)
	transfer(users[3], users[2], 1)

def printTransactionLog():
	print("\nTransaction Log: ")
	for t in transactionLog:
		print("%s \tto \t%s \t(%d) \t Funds pre/post: (%d/%d, %d/%d)" 
			% (t.sender.name, 
				t.recipient.name, 
				t.amount, 
				t.senderFundsPre, 
				t.senderFundsPre-t.amount,
				t.recipientFundsPre, 
				t.recipientFundsPre+t.amount))

# BEGIN
users = createUsers()
printAllUsers(users)
# Transactions
transactionLog = []
performBasicTransactions(users)
printAllUsers(users)

performUnevenTransactions(users)
printAllUsers(users)

printTransactionLog()