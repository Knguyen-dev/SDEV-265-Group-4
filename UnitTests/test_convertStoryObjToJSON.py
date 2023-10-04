import unittest
import sys
sys.path.append("..")
from classes.models import Story, Message 
from classes.utilities import convertStoryObjToJSON

class TestConvertStoryObjToJSON(unittest.TestCase):

    def testJSON(self):
        storyObj = Story(
            storyTitle="The Mysterious Pendant",
            messages=[
                Message(text="In a distant land", isAISender=True),
                Message(text="Lived a young adventurer named Alex", isAISender=False),
                Message(text="One day, Alex found a pendant", isAISender=True),
                Message(text="Little did they know, the pendant held ancient powers", isAISender=False),
            ]
        )

        storyJSON = [
			{"role": "assistant", "content": "In a distant land"},
			{"role": "user", "content": "Lived a young adventurer named Alex"},
			{"role": "assistant", "content": "One day, Alex found a pendant"},
			{"role": "user", "content": "Little did they know, the pendant held ancient powers"},
		]

        self.assertEqual(convertStoryObjToJSON(storyObj), storyJSON)