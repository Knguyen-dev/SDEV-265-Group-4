import unittest
import sys
sys.path.append("..")
from classes.utilities import isValidUsername

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