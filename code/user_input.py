# Ruby Bron       12474223
# Sophie Stiekema 10992499
# Michael Stroet  11293284

def is_integer(string):
	'''
	Determines if the given string represents a integer
	'''
	try:
		int(string)
		return True
	except ValueError:
		return False


def is_float(string):
	'''
	Determines if the given string represents a float
	'''
	try:
		float(string)
		return True
	except ValueError:
		return False


def ask_integer(message):
	'''
	Asks the user for an integer
	'''
	user_input = input(message)

	while not is_integer(user_input):
		user_input = input(message)

	return int(user_input)


def ask_float(message):
	'''
	Asks the user for a float
	'''
	user_input = input(message)

	while not is_float(user_input):
		user_input = input(message)

	return float(user_input)
