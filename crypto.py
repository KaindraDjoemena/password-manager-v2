import random
from random import choices

# The cryptography class
class Crypto:
	
	# This sets the length of the random values and 10 chars is its default length
	def __init__(self, length=10):
		self.length = length

	# This method makes the key
	def makeKey(self):
		# The keys
		value_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890`~!@#$%^&*()-_=+[]|;:,<.>/?"
		
		# The values
		characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890`~!@#$%^&*()-_=+[]|;:,<.>/?"

		key_dict = dict() # < Making an empty dict

		# Assigns random chars from characters and concat them for them to be
		# assign to on of the keys
		for char in value_characters:
			random_value = ""
			if char == value_characters[0]:
				for times in range(self.length):
					random_char = random.choice(characters)
					random_value += random_char
				key_dict[char] = random_value
			for key_char, value in key_dict.items():
				random_value = ""
				for times in range(self.length):
					random_char = random.choice(characters)
					random_value += random_char

				# If the random value is equal to one of the values inside the dict,
				# then generate another one
				while random_value == value:
					random_value = ""
					for times in range(self.length):
						random_char = random.choice(characters)
						random_value += random_char
			key_dict[char] = random_value # < Adds the key and the random value pair to the dict
		return key_dict

	# This method encrypts the message "x"
	def encrypt(self, x, key):
		encrypted_word = ""
		char_list = list(x) # < Converting the string into a list
		for char in char_list:
			conv_char = key[char] # < For every index of the list/char, we turn it into the matching key's value
			encrypted_word += conv_char
		return encrypted_word

	#this method decrypts the ecrypted message "x"
	def decrypt(self, x, key):
		decrypted_message = ""
		seperated_enc_char = [x[i:i+self.length] for i in range(0, len(x), self.length)] # < Devides it by chunks
		for enc_char in seperated_enc_char: # < Converts every chunk into chars
			for letter, value in key.items():
				if enc_char == value:
					decrypted_message += letter
		return decrypted_message
