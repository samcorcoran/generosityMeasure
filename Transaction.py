import math
import random

class Transaction():
	def __init__(self, sender, recipient, amount):
		self.sender = sender
		self.recipient = recipient
		self.amount = amount
		self.senderFundsPre = sender.points
		self.recipientFundsPre = recipient.points
		self.executed = False

	def execute(self):
		self.sender.points -= self.amount
		self.recipient.points += self.amount
		self.executed = True
