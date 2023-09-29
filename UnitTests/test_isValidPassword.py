import unittest
import sys
sys.path.append("..")
from classes.utilities import isValidPassword

class TestIsValidPassword(unittest.TestCase):

	def testValidPasswords(self):
		validPasswords = ["asdfjk", "qejfj1092", "HJi109meno" , "w!s@jei#$", "%^hu&*an()", "L{@#s3j2value_}[]!~,"]
		for password in validPasswords:
			with self.subTest(password=password):
				self.assertTrue(isValidPassword(password))

	def testInvalidPasswords(self):
		invalidPasswords = ["", "short", "password with space", "long-pass-that-is-over-limit"]
		for password in invalidPasswords:
			with self.subTest(password=password):
				self.assertFalse(isValidPassword(password))

if __name__ == "__main__":
	unittest.main()