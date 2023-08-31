import unittest
import re
def isValidUsername(username):
	# An alphanumeric username that is 6 to 20 characters long, accepts underscores
	pattern = r'^\w{6,20}$'
	return re.match(pattern, username) is not None

class TestIsValidUsername(unittest.TestCase):
	def testValidUsernames(self):  
		validUsernames = ["username", "uSerName" ,"Short45", "UPPERNAME", "Long_User_Name4_1289"]
		for username in validUsernames:
			with self.subTest(username=username):
				self.assertTrue(isValidUsername(username))
	
	def testInvalidUsernames(self):
		invalidUsernames = ["", "short", "$DonnaPerol", "Some-username@guy", "long-username-over-limit"]
		for username in invalidUsernames:
			with self.subTest(username=username):
				self.assertFalse(isValidUsername(username))

if __name__ == "__main__":
	unittest.main()