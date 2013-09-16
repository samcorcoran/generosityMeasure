import math
import random

# Creates a list of dictionaries, each containing a transaction
def generateFakeTransactionLog(n):
	log = []
	users = {'Sam': 10, 'Will': 10, 'Ben': 10, 'Andy': 10}
	for i in xrange(n):
		print(i)
		# Pick a 'from' user who has at least some points
		fromUser = random.choice(users.keys())
		while not users[fromUser] > 0:
			print("Picking a from")
			fromUser = random.choice(users.keys())
		# Pick a 'to' user who is not the already selected user1
		toUser = random.choice(users.keys())
		while fromUser == toUser:
			print("Picking a to")
			toUser = random.choice(users.keys())
		# Determine the size of the transaction
		transactionAmount = random.randint(1, users[fromUser])
		print("Transaction amount: " + str(transactionAmount))
		log.append({'from': fromUser, 'fromPoints': users[fromUser], 'to': toUser, 'toPoints': users[toUser], 'amount': transactionAmount})
		# Updates amount
		users[fromUser] -= transactionAmount
		users[toUser] += transactionAmount
	return log

# Great a fake transaction log
numTransactions = 10
transactionLog = generateFakeTransactionLog(numTransactions)

# Print transaction log
for entry in transactionLog:
	print(entry)

# Create a dictionary of username keys and generosity values
def calculateGenerosities(tLog):
	print("Calculating generosities")
	generosities = dict()
	for t in tLog:
		generosity = 0
		# Add generosity to existing user entry
		if t["from"] in generosities:			
			print(generosities)
			generosities[t["from"]] += generosity
		# Add new user to dictionary
		else:
			generosities[t["from"]] = generosity

	return generosities

generosities = calculateGenerosities(transactionLog)

for entry in generosities:
	print(entry)