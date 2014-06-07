
import challenge

class EasyAlarm(challenge.Challenge):
	
	def __init__(self):
		challenge.Challenge.__init__(self, "EasyAlarm")
		self.correctAnswer = [1,2,3,4]
		
	def handle_query(self, parameters):
		result = ["naq", []]
		
		if len(parameters) < 2:
			result[1] = "not enough parameters"
			return result
		
		query_type = parameters[0]
		
		if query_type == "test":
			number = None
			try:
				number = int(parameters[1])
			except:
				result[1] = "invalid test number input"
				return result
			if number < 0 or number > 9:
				result[1] = "invalid test number input"
				return result
			result[0] = "ack"
			result[1] = self.generate_pattern([number])
		elif query_type == "sequence":
			numbers = []
			if parameters[1] == "correct":
				numbers = self.correctAnswer
			else:
				for num in parameters[1]:
					try:
						numbers.append(int(num))
					except:
						result[1] = "invalid number sequence"
						return result
			result[0] = "ack"
			result[1] = [self.generate_pattern(numbers)]
		else:
			result[1] = "invalid query type"
		
		return result
	
	def generate_pattern(self, numbers):
		bits = ""
		bitsPerNumber = 4
		
		symbolBits = 10
		spaceBits = 40
		for space in range(spaceBits):
			bits += "0"
		
		for number in numbers:
			for symbol in range(symbolBits):
				bits += "1"
			for bit in range(bitsPerNumber-1, -1, -1):
				value = str((number >> bit) & 0x1)
				for symbol in range(symbolBits):
					bits += value
			for space in range(spaceBits):
				bits += "0"
		
		return bits
