import unittest
import sys
sys.path.append("..")
from classes.models import Message
from classes.utilities import convertMessageObjToJSON

class TestConvertMessageObjToJSON(unittest.TestCase):
	def testJSON(self):
		# Array of message objects that we're testing 
		messageObjList = [
			Message(text="In a distant land", isAISender=True),	
			Message(text="Lived a young adventurer named Alex", isAISender=False),
			Message(text="One day, Alex found a pendant", isAISender=True),
			Message(text="Little did they know, the pendant held ancient powers", isAISender=False),
		]
		# Parallel list that represents the corresponding expected return value from the conversion function
		messageJSONList = [
			{"role": "assistant", "content": "In a distant land"},
			{"role": "user", "content": "Lived a young adventurer named Alex"},
			{"role": "assistant", "content": "One day, Alex found a pendant"},
			{"role": "user", "content": "Little did they know, the pendant held ancient powers"},
		]
		for messageObj, messageJSON in zip(messageObjList, messageJSONList):
			with self.subTest(messageObj=messageObj, messageJSON=messageJSON):
				self.assertDictEqual(convertMessageObjToJSON(messageObj), messageJSON)

if __name__ == "__main__":
	unittest.main()