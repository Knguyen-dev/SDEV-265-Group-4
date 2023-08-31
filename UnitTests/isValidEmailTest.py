import unittest
import re

def isValidEmail(email):
	pattern = r'^[\w\.-]+@\w+\.\w+$'
	return re.match(pattern, email) is not None

class TestIsValidEmail(unittest.TestCase):
	
	def testValidEmails(self):
		validEmails = [ "knguyen@gmail.com", "AkaM0ped@ivytech.edu", "Rainbow_Dragon@co.uk", "user.name@example.com", "contact-info@domain.co", "support123.Konami@outlook.com"]
		for email in validEmails:
			with self.subTest(email=email):
				self.assertTrue(isValidEmail(email))
	
	def testInvalidEmails(self):
		invalidEmails = ["", "@email.com", "s0meGmail.com", "someone@example", "otheremail@mail.", "bad-email-co"]
		for email in invalidEmails:
			with self.subTest(email=email):
				self.assertFalse(isValidEmail(email))

if __name__ == "__main__":
	unittest.main()