import math
import random

class Transaction():
	def __init__(self, sender, recipient, amount):
		self.sender = sender
		self.recipient = recipient
		self.amount = amount
		self.senderFundsPre = sender.points
		self.recipientFundsPre = recipient.points
		self.transactionGenerosity = 0
		self.executed = False

	def execute(self):
		self.sender.points -= self.amount
		self.recipient.points += self.amount
		self.sender.generosity += self.generosity
		# Track points given/received, for reference
		self.sender.totalPointsGiven += self.amount
		self.recipient.totalPointsReceived += self.amount
		self.executed = True


	def printTransaction(self):
		print("%s \tto \t%s \t(%d) \t Funds pre/post: (%d/%d, %d/%d) Generosity: %f" 
			% (self.sender.name, 
				self.recipient.name, 
				self.amount, 
				self.senderFundsPre, 
				self.senderFundsPre-self.amount,
				self.recipientFundsPre, 
				self.recipientFundsPre+self.amount,
				self.generosity))