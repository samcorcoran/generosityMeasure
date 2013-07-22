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

def transfer(sender, recipient, points):
	# Restrict to integer transfers
	if not isinstance(points, int):
		return False
	# validate amount
	if not (points > 0 or points <= sender.points):
		return False
	# Create transaction
	transaction = Transaction.Transaction(sender, recipient, points)
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
		print("%s \tto \t%s \t(%d) \t Previous funds: (%d, %d)" % (t.sender.name, t.recipient.name, t.amount, t.senderFundsPre, t.recipientFundsPre))

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