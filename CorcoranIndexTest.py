import random

import CorcoranIndex

# Creates a list of dictionaries, each containing a transaction
def generateFakeTransactionLog(n):
	log = []
	users = {'Sam': 10, 'Will': 10, 'Ben': 10, 'Andy': 10}
	economySize = 40
	totalUsers = 4
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
		log.append({'from': fromUser, 'fromPoints': users[fromUser], 'to': toUser, 'toPoints': users[toUser], 'amount': transactionAmount, 'economySize': economySize, 'totalUsers': totalUsers})
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

generosities = CorcoranIndex.calculateGenerosities(transactionLog)

print(generosities)
