import uuid

class User():
	def __init__(self, userName, points=10):
		self.name = userName
		self.id = uuid.uuid4()
		self.points = points
		self.generosity = 0
		self.totalPointsGiven = 0
		self.totalPointsReceived = 0

	def printInfo(self):
		print("  User name: ", self.name)
		print("    ID: ", self.id)
		print("    Points: ", self.points)
		print("    Generosity: ", self.generosity)