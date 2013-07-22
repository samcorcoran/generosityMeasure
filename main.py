import math
import random
import Users

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

users = createUsers()
printAllUsers(users)