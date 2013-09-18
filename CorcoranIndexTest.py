import random

import CorcoranIndex

# Creates a list of dictionaries, each containing a transaction
def generateFakeTransactionLog(n):
	log = []
	users = {'Sam': 0, 'Will': 0, 'Ben': 0, 'Andy': 0, 'wangbot': 1}
	for i in xrange(n):
		# Pick a 'from' user who has at least some points
		fromUser = random.choice(users.keys())
		while not users[fromUser] > 0 and not fromUser == 'wangbot':
			#print("Picking a from")
			fromUser = random.choice(users.keys())
		# Pick a 'to' user who is not the already selected user1
		toUser = random.choice(users.keys())
		while fromUser == toUser:
			#print("Picking a to")
			toUser = random.choice(users.keys())
		# Determine the size of the transaction
		transactionAmount = random.randint(1,20)
		if not fromUser == 'wangbot':
			transactionAmount = random.randint(1, users[fromUser])
		#print("Transaction amount: " + str(transactionAmount))
		log.append({'from': fromUser, 'to': toUser, 'amount': transactionAmount})
		# Updates amount
		if fromUser != 'wangbot':
			users[fromUser] -= transactionAmount
		users[toUser] += transactionAmount
	return log

# Great a fake transaction log
numTransactions = 100
transactionLog = generateFakeTransactionLog(numTransactions)

# Print transaction log
# for entry in transactionLog:
# 	print(entry)

generosities, transactionCounts = CorcoranIndex.calculateGenerosities(transactionLog)

totalGenerosity = sum(generosities.values())
for user in generosities.keys():
	avgGenerosity = 'NA' 
	if user in transactionCounts and transactionCounts[user] > 0:
		avgGenerosity = generosities[user]/float(transactionCounts[user])
	print("%s: \t%f (Average generosity: %s)" % (user, generosities[user]/float(totalGenerosity), avgGenerosity))