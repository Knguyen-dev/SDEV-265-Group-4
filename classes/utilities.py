# Accepts list of entry widgets and clears their input
from tkinter import END
import customtkinter as ctk
import re


'''
- Clears entry widgets of any input
'''
def clearEntryWidgets(entryWidgets):
    for entry in entryWidgets:
        entry.delete(0, END)

'''
- Toggles whether or not an entry widget's input is hidden, accepts a checkbox. Currently used to hide the value 
	in password entry fields
'''
def toggleHidden(entryWidget, checkVar):
	# If it's checked, user wants to hide password
	if checkVar.get() == "on":
		entryWidget.configure(show="*")
	else:
		entryWidget.configure(show="")

'''
- strips the input of entry widget of trailing or leading whitespace
'''
def stripEntryWidgets(entryWidgets):
	strippedWidgets = []
	for entry in entryWidgets:
		inputValue = entry.get().strip()
		entry.delete(0, END)
		entry.insert(0, inputValue)
		strippedWidgets.append(entry)
	return strippedWidgets

'''
- Checks if any one of the entry widgets in the list entryWidgets has no input
'''
def isEmptyEntryWidgets(entryWidgets):
	entryWidgets = stripEntryWidgets(entryWidgets) # strip for spaces 
	for entry in entryWidgets:
		if entry.get() == "":
			return True
	return False

'''
- Checks if email matches the regex pattern

1. First bracket means it can be more than one alphanumeric synbol and underscore. Also accepts periods
	and hypens.
2. Second section checks if it has an @ symbol and then some letters behind it, as a domain name "@gmail" "@outlook"
3. Lastly it checks a period so it checks things like ".com" or ".edu"

'''
def isValidEmail(email):
	pattern = r'^[\w\.-]+@\w+\.\w+$'
	return re.match(pattern, email) is not None

# Ensures password follows rules: 6-20 characters, numbers, letters, symbols, no spaces
def isValidPassword(password):
	pattern = r'^[\w!@#$%^&*(){}<>\,\~\+\~\-\.\[\]]{6,20}$'
	return re.match(pattern, password)

# Ensures username is valid
def isValidUsername(username):
	# An alphanumeric username that is 6 to 20 characters long, accepts underscores
	pattern = r'^\w{6,20}$'
	return re.match(pattern, username) is not None

# Converts message object to openai json message format 
def convertMessageObjToJSON(messageObj):
	messageJSON = {"role": "", "content": f"{messageObj.text}"}
	if messageObj.isAISender:
		messageJSON["role"] = "assistant"
	else:
		messageJSON["role"] = "user"
	return messageJSON

# Converts story object to openai json format
def convertStoryObjToJSON(storyObj):
	storyJSON = []
	for messageObj in storyObj.messages:
		storyJSON.append(convertMessageObjToJSON(messageObj))
	return storyJSON


def add_testing_functions(Class):
		'''
		- Mimics sendStoryPrompt by adding the user's and AI's messages to chat history. Of course while 
		it's doing this, it'll return a generator that yields the message content.
		'''
		def mockSendStoryPrompt(self, userMessage: str):
			self.addMessageAt(userMessage, len(self.chat), "user")
			chunks = [
				"This is a sample message chunk. This",
				" is the second send story chunk.",
				" Here is the third one!"
			]
			message = ""
			for chunk in chunks:
				message += chunk
				yield chunk
			self.addMessageAt(message, len(self.chat), "assistant")


		'''
		- Mimics the processes in sendRemixPrompt for chat history. The user sends the ai a message, then AI returns a
		 generator in response. AI will store the remix message in its chat history.
		'''
		def mockRemixStory(self):
			# Simulate the returning of chunks in a generator
			chunks = [
				"This is a remix message chunk. This",
				" is the second remix chunk.",
				" This is the last remix chunk we'll have!"
			]
			message = ""
			for chunk in chunks:
				message += chunk
				yield chunk
			self.addMessageAt(message, len(self.chat), "assistant")

		def mockPrint(self):
			print("Hey it worked!")

		Class.mockSendStoryPrompt = mockSendStoryPrompt
		Class.mockRemixStory = mockRemixStory
		Class.mockPrint = mockPrint
		return Class