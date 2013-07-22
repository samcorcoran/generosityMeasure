import math
import random
import uuid

class User():
	def __init__(self, userName, points=10):
		self.name = userName
		self.id = uuid.uuid4()
		self.points = points

	def printInfo(self):
		print("  User name: ", self.name)
		print("    ID: ", self.id)
		print("    Current points: ", self.points)