# Tkinter itself
import tkinter as tk
import customtkinter as ctk 
# Import our models
from classes.models import *
# import utility functions
from classes.utilities import *
# Import hash library for hashing passwords
import hashlib
# Import sqlalchemy to do our operations
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
# For creating a dynamic footer 
import datetime
# For image rendering
from PIL import Image, ImageTk
import os			



ctk.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"

'''
NOTE: For functionality such as continuing a story. We need to keep track of the 
messages the user is typing in. If they type in a message, and then go to another page, we'll
need to remember what messages they typed. If there isn't an ai function for this, we 
can keep track of the user's messages in the "App" class with an array of Message Objects. So 
next time the user clicks "Continue story" we just load in the ai chat page with the message objects 
from 'App', which will render those messages in.

- Also for saving a story, we'll just access the messages in 'App' as those are the messages 
from the story that the user wants to save

- For continuing a saved story, we'll set obviously load those messages into the ai chat page 
class for rendering, but also we'll make those messages as the messages for the current session 
or story. So if user clicks off of a page, those messages are now the recent ones and the ones they 
left off on.


- The reason for only passing "Message" objects to the ai chat page is because it
not needed. We don't want to create a story object everytime because when you're in the ai chat page,
you haven't automatically created a story with a title. You
have some story, that may or may not be saved. Only when you click the save button, do you actually get
to choose the title of the story.

'''





class homePage(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master

		innerPageFrame = ctk.CTkFrame(self, fg_color="transparent")

		pageHeader = ctk.CTkFrame(innerPageFrame, fg_color="transparent")
		pageHeading = ctk.CTkLabel(pageHeader, text="Home", font=("Helvetica", 32))

		pageBtnsSection = ctk.CTkFrame(innerPageFrame, fg_color="transparent")
		newStoryBtn = ctk.CTkButton(pageBtnsSection, text="Start A New Story!")
		continuePrevStoryBtn = ctk.CTkButton(pageBtnsSection, text="Continue Previous Story!")

		innerPageFrame.pack(expand=True)
		pageHeader.grid(row=0, column=0, pady=10)
		pageHeading.grid(row=0, column=0)

		pageBtnsSection.grid(row=1, column=0)
		newStoryBtn.grid(row=0, column=0, pady=5)
		continuePrevStoryBtn.grid(row=1, column=0, pady=5)


	'''
	+ startNewStory: 
		- When we start a new story, we are starting a new chat. 
		All messages from the previous chat/session, should be deleted. As well as 
		this, when we open the ai chat page, we should not pass any message objects to its class, so it has no previous 
		messages to render. 

	+ continuePrevStory:
		- When we continue a previous story, we are continuing 
		the most recent chat session that the user had. We 
		direct the user to the chat page, passing all of the messages, as
		message objects to the chat page class so that the chat page can render those messages appropriately.
	'''
	def startNewStory(self):
		# Clear chat messages from the previous or most recent session since we're starting a new story/chat
		
		# Redirect the user to the ai chat page, and don't pass in anything for the 'Messages' argument that 
		# we plan the ai chat page to have
		pass

	def continuePrevStory(self):
		# Get the chat messages from the most recent session/chat

		# Redirect the user to the ai chate page, and pass these messages in order for them to be already rendered.
		pass


			


'''
+ Page for remixing an existing story. This page is passed
	a story object (from the storyLibraryPage) that represents the story we're remixing.
	Using this existing story, and the user's input saying how 
	the story will be remixed, we send both to the AI. The 
	AI then sends back a generated message to this class. Then we redirect 
	the user to the ai chat page and pass in the ai's message (this starts a new chat).

'''
class remixStoryPage(ctk.CTkFrame):
	def __init__(self, master, story):
		super().__init__(master)
		self.master = master
		self.story = story

		form = ctk.CTkFrame(self)

		formHeader = ctk.CTkFrame(form, fg_color="transparent")
		formHeading = ctk.CTkLabel(formHeader, text="Remix A Story", font=("Helvetica", 32))
		subheading = ctk.CTkLabel(formHeader, text=f"Currently Remixing '{story.storyTitle}'!", wraplength=200)

		formFieldsSection = ctk.CTkFrame(form)
		label = ctk.CTkLabel(formFieldsSection, text="Enter your twist on this story!", wraplength=100)
		self.remixInput = ctk.CTkTextbox(formFieldsSection)

		formBtnsSection = ctk.CTkFrame(form)
		clearRemixBtn = ctk.CTkButton(formBtnsSection, text="Clear", command=lambda: self.remixInput.delete("0.0", "end"))
		remixStoryBtn = ctk.CTkButton(formBtnsSection, text="Confirm Remix", command=self.remixStory)

		form.pack(expand=True)
		formHeader.grid(row=0, column=0, pady=10, padx=50)
		formHeading.grid(row=0, column=0)
		subheading.grid(row=1, column=0)
		formFieldsSection.grid(row=1, column=0, pady=10)
		label.grid(row=0, column=0, pady=10)
		self.remixInput.grid(row=1, column=0, pady=10)
		formBtnsSection.grid(row=2, column=0, pady=10)
		clearRemixBtn.grid(row=0, column=0, padx=10)
		remixStoryBtn.grid(row=0, column=1, padx=10)


	'''
	+ remixStory: Remixes a story using an existing story and user's input. Then takes the user to the ai chat page for the remixed story
	'''
	def remixStory(self):

		# Get the text of the remix
		remix = self.remixInput.get("0.0", "end")

		'''
		- Assume there's a function, pass the ai the story's messages and then the 'remix' text. You're 
		expected a response message, a string, so store it in 'responseMessage' or something similar. 
		It should be something similar to this: 
		'''
		# responseMessage = storyAI.remixStory(remix, messages)

		# Then turn 'responseMessage' into a Message object and put responseMessage into an array
		# so that you can pass it into the ai chat page's class

		# Then redirect the user to the ai chat page, pass in our array that has "responseMessage" message object



'''
+ saveStoryPage: Page where the user will save a story, which should be the most recent story that they 
had on the chat page. The chat page, would redirect the user to the saveStoryPage. 

'''
class saveStoryPage(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master

		form = ctk.CTkFrame(self)
		
		formHeader = ctk.CTkFrame(form, fg_color="transparent")
		formHeading = ctk.CTkLabel(formHeader, text="Save Story", font=("Helvetica", 32))
		self.formErrorMessage = ctk.CTkLabel(formHeader, text="")

		formFieldsSection = ctk.CTkFrame(form)		
		label = ctk.CTkLabel(formFieldsSection, text="Story Title")
		self.storyTitleEntry = ctk.CTkEntry(formFieldsSection)

		formBtnsSection = ctk.CTkFrame(form, fg_color="transparent")
		clearFormBtn = ctk.CTkButton(formBtnsSection, text="Clear", command=lambda: clearEntryWidgets([self.storyTitleEntry]))
		saveStoryBtn = ctk.CTkButton(formBtnsSection, text="Save Story", command=self.saveStory)

		# Structure the remaining elements of the page
		form.pack(expand=True)
		formHeader.grid(row=0, column=0, pady=10, padx=80)
		formHeading.grid(row=0, column=0)
		self.formErrorMessage.grid(row=1, column=0)
		formFieldsSection.grid(row=1, column=0, pady=10)
		label.grid(row=0, column=0, pady=10, padx=10)
		self.storyTitleEntry.grid(row=0, column=1, pady=10, padx=10)
		formBtnsSection.grid(row=2, column=0, pady=10)
		clearFormBtn.grid(row=0, column=0, padx=10)
		saveStoryBtn.grid(row=0, column=1, padx=10)


	# Saves a story to the user's library of stories
	def saveStory(self):
		# Check if fields are empty, put the entry widget in an array so that the function works
		if (isEmptyEntryWidgets([self.storyTitleEntry])):
			self.formErrorMessage.configure(text="Some fields are empty!")
			return
		
		# Get messages of the most recent chat from the ai, because
		# that is where the user was writing their story with the AI.
		# This would be "self.master.currentStoryMessages"

		# Create a Story object with the user's inputted title

		# Create Message objects from all of the chat's messages 

		# Now assign/put those message objects in the story object

		# Save the story to the database, in the stories table

		# Redirect the user to the storyLibraryPage, which is where their new story should be
		self.master.openPage("storyLibraryPage") #type: ignore



# Ai settings page frame
class aiSettingsPage(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		form = ctk.CTkFrame(self)

		# Form header
		formHeader = ctk.CTkFrame(form, fg_color="transparent")
		formHeading = ctk.CTkLabel(formHeader, text="Configure AI Settings!", font=("Helvetica", 32))
		
		# Section for form sliders 
		formFieldsSection = ctk.CTkFrame(form)
		self.formSlidersList = [] #list of sliders
		'''
		NOTE: The "value" attribute in the formFields objects/maps should be obtained from the 
			ai chat bot that we instantiate.
		''' 
		formFields = [ # array of objects for the creation of the form sliders
			{
				"text": 'Temperature',
				"lower": 1,
				"upper": 10,
				"value": 5,
			},
			{
				"text": 'Top P',
				"lower": 1,
				"upper": 10,
				"value": 5,
			},
			{
				"text": 'Top K',
				"lower": 1,
				"upper": 10,
				"value": 5,
			},
			{
				"text": 'Presence Penalty',
				"lower": 1,
				"upper": 10,
				"value": 5,
			},
			{
				"text": 'Frequency Penalty',
				"lower": 1,
				"upper": 10,
				"value": 5,
			},
		]

		# Create form sliders and labels iteratively
		for x in range(len(formFields)):
			sliderVar = tk.IntVar() # tkinter variable to keep track and display a slider's value
			sliderVar.set(formFields[x]["value"]) # set the starting value of the tkinter variable, and as a result the slider itself
			label = ctk.CTkLabel(formFieldsSection, text=formFields[x]["text"]) # label defining what a slider is for
			sliderValueLabel = ctk.CTkLabel(formFieldsSection, textvariable=sliderVar) # label defining what value a slider is currently on
			slider = ctk.CTkSlider(formFieldsSection, from_=formFields[x]["lower"], to=formFields[x]["upper"], variable=sliderVar) # tkinter slider widget
			label.grid(row=x, column=0, padx=10, pady=10)
			sliderValueLabel.grid(row=x, column=1, padx=10, pady=10)
			slider.grid(row=x, column=2, padx=10, pady=10)
			self.formSlidersList.append(slider)

		# Create the form buttons
		formBtnsSection = ctk.CTkFrame(form, fg_color="transparent")
		restoreSettingsBtn = ctk.CTkButton(formBtnsSection, text="Restore Settings")
		changeSettingsBtn = ctk.CTkButton(formBtnsSection, text="Confirm Changes")

		# Structure the widgets on the page
		form.pack(expand=True)		
		formHeader.grid(row=0, column=0, pady=10)
		formHeading.grid(row=0, column=0)
		formFieldsSection.grid(row=1, column=0, pady=10, padx=10)
		formBtnsSection.grid(row=2, column=0, pady=10)
		restoreSettingsBtn.grid(row=0, column=0, padx=10)
		changeSettingsBtn.grid(row=0, column=1, padx=10)
	

	# Restores the value of the sliders to represent what the AI chat bot 
	# is currently using.
	def restoreAISettings(self):
		pass


	# Changes the settings of the AI chat bot
	def changeAISettings(self):
		pass


class storyLibraryPage(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master

		# Inner page frame for centering content at center of storyLibraryPage frame
		innerPageFrame = ctk.CTkScrollableFrame(self, fg_color="transparent", width=525, height=500)
		innerPageFrame.pack(expand=True)
		
		# Get the saved stories, from the logged in user, if there are any
		savedStories = self.master.loggedInUser.stories

		# If there aren't any stories saved, then just show a message, and stop it early
		if not savedStories:
			label = ctk.CTkLabel(innerPageFrame, text="No stories have been saved yet!", font=("Helvetica", 24))
			label.pack()
			return

		rowIndex = 0
		columnIndex = 0
		# At this point, there are stories, so iteratively create 'cards' or containers that display
		# their information
		for story in savedStories:
			storyCard = ctk.CTkFrame(innerPageFrame, fg_color="#7dd3fc", width=200)

			# columnIndex number of story cards per row
			# if true, then columnIndex story cards have already been placed, so reset
			# the column index, and move on to a new row
			if (columnIndex == 3):
				columnIndex = 0
				rowIndex += 1

			cardHeader = ctk.CTkFrame(storyCard)
			cardTitle = ctk.CTkLabel(cardHeader, fg_color="#7dd3fc", text=f"Title: {story.storyTitle}", wraplength=200)
			cardBody = ctk.CTkFrame(storyCard, fg_color="#7dd3fc")
			continueSavedStoryBtn = ctk.CTkButton(cardBody, text="Continue", command=lambda story=story: self.continueSavedStory(story))
			openRemixStoryBtn = ctk.CTkButton(cardBody, text="Remix", command=lambda story=story: self.master.openPage("remixStoryPage", story))  #type: ignore
			deleteSavedStoryBtn = ctk.CTkButton(cardBody, text="Delete", command=lambda story=story: self.deleteSavedStory(story))
			
			# Structure the storyCard and its widgets
			storyCard.grid(row=rowIndex, column=columnIndex, padx=10, pady=10)
			cardHeader.grid(row=0, column=0, pady=10)
			cardTitle.grid(row=0, column=0)
			cardBody.grid(row=1, column=0)
			continueSavedStoryBtn.grid(row=0, column=0, pady=5)
			openRemixStoryBtn.grid(row=1, column=0, pady=5)
			deleteSavedStoryBtn.grid(row=2, column=0, pady=5)

			# Increment column count
			columnIndex += 1
		
	'''
	+ continueSavedStory: 
		Get the messages of the story object and pass them into the ai chat page's class while we redirect them, 
		so those old messages can be rendered. As a result, the user is allowed to continue where they left off
	'''
	def continueSavedStory(self, story):
		# The messages from the saved story become the messages for the current session
		self.master.currentStoryMessages = story.messages #type: ignore

		# Then redirect the user to the ai chat page now that we've updated the messages we want to render



	
	# Deletes a story from the user's library
	def deleteSavedStory(self, story):
		# Delete story from database
		self.master.session.delete(story) #type: ignore
		self.master.session.commit() #type: ignore
		# Reload the story library page
		self.master.openPage("storyLibraryPage") #type: ignore	




class editAvatarPage(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		innerPageFrame = ctk.CTkFrame(self)
		
		self.imageFolderPath = "./assets/images/" # Path to image folder 
		self.imageIndex = 0 # Index of the current image
		self.imageList = self.getImageFileNames() # list of image file names that we'll use to load images 
		self.currentImageFileName = "" # the file name of the current image file the image slider is on

		# Heading of the page
		header = ctk.CTkFrame(innerPageFrame)
		heading = ctk.CTkLabel(header, text="Choose your avatar or pfp", font=("Helvetica", 32))

		# Create image label where we'll display the image
		self.imageLabel = tk.Label(innerPageFrame)

		# Create container and buttons for the image slider
		imageBtnsSections = ctk.CTkFrame(innerPageFrame)
		prevImageBtn = ctk.CTkButton(imageBtnsSections, text="Previous", command=self.loadPreviousImage)
		nextImageBtn = ctk.CTkButton(imageBtnsSections, text="Next", command=self.loadNextImage)
		selectImageBtn = ctk.CTkButton(imageBtnsSections, text="Select", command=self.changeAvatar)

		# Structure the widgets 
		innerPageFrame.pack(expand=True)
		header.grid(row=0, column=0, pady=10)
		heading.grid(row=0, column=0)

		self.imageLabel.grid(row=1, column=0, pady=10)

		imageBtnsSections.grid(row=2, column=0, pady=10)
		prevImageBtn.grid(row=0, column=0, padx=10)
		nextImageBtn.grid(row=0, column=1, padx=10)
		selectImageBtn.grid(row=0, column=2, padx=10)

		# Load the current image onto the screen
		self.loadCurrentImage()

	# Returns the paths of all of the image files in a list
	def getImageFileNames(self):
		fileNames = os.listdir(self.imageFolderPath) 
		return [fileName for fileName in fileNames]
		
	# Loads the current image onto the screen
	def loadCurrentImage(self):
		# Put new image on the label to display it
		newImage = ImageTk.PhotoImage(Image.open(f"{self.imageFolderPath}{self.imageList[self.imageIndex]}").resize((300, 300)))
		self.imageLabel.configure(image=newImage)
		self.imageLabel.image = newImage #type: ignore

		# Update the file name of the current image
		self.currentImageFileName = self.imageList[self.imageIndex]

	# Loads the next image
	def loadNextImage(self):
		self.imageIndex += 1
		if (self.imageIndex > len(self.imageList) - 1):
			self.imageIndex = 0
		self.loadCurrentImage()

	# Loads the previous image
	def loadPreviousImage(self):
		self.imageIndex -= 1
		if (self.imageIndex < 0):
			self.imageIndex = len(self.imageList) - 1
		self.loadCurrentImage()


	# Changes the avatar of the currently logged in user
	def changeAvatar(self):
		# Update the avatar attribute with the image's file name, and persist that change to the database
		self.master.loggedInUser.avatar = self.currentImageFileName #type: ignore
		self.master.session.commit() # type: ignore

		# Redirect the user to the account page to make sure they see their changess
		self.master.openPage("userAccountPage") #type: ignore




##### Page for changing passwords #####
class changePasswordPage(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master

		# Create edit form frame
		form = ctk.CTkFrame(self)
		form.pack(expand=True)

		# Create header of the form
		formHeader = ctk.CTkFrame(form, fg_color="transparent")
		formHeading = ctk.CTkLabel(formHeader, text="Change Password", font=("Helvetica", 32))
		self.formErrorMessage = ctk.CTkLabel(formHeader, text="")
		
		# Create the input section with form fields 
		formFieldsSection = ctk.CTkFrame(form)

		formFields = [
			"Old Password",
			"New Password",
			"Retype New Password",
		]
		# Create list of form entries to get input later
		# Then create and position label and entry widgets for form
		self.formEntryList = []
		for x in range(len(formFields)):
			label = ctk.CTkLabel(formFieldsSection, text=formFields[x])
			entry = ctk.CTkEntry(formFieldsSection)
			checkVar = ctk.StringVar(value="off")
			visibilityCheckBox = ctk.CTkCheckBox(formFieldsSection, variable=checkVar, command=lambda entry=entry, var=checkVar: toggleHidden(entry, var),  text="Hide", onvalue="on", offvalue="off")
			self.formEntryList.append(entry)
			label.grid(row=x, column=0, pady=10, padx=10)
			entry.grid(row=x, column=1, pady=10, padx=10)
			visibilityCheckBox.grid(row=x, column=2, pady=10, padx=4)

		# Create section to have form buttons/actions
		formBtnsSection = ctk.CTkFrame(form, fg_color="transparent")
		clearFormBtn = ctk.CTkButton(formBtnsSection, text="Clear", command=lambda: clearEntryWidgets(self.formEntryList))		
		changePasswordBtn = ctk.CTkButton(formBtnsSection, text="Confirm Change", command=self.changePassword)

		# Structure the remaining elements of the page
		# padx=90; adds enough gray padding so that form looks uniform
		formHeader.grid(row=0, column=0, pady=10, padx=90)
		formHeading.grid(row=0, column=0)
		self.formErrorMessage.grid(row=1, column=0)
		formFieldsSection.grid(row=1, column=0, pady=10)
		formBtnsSection.grid(row=2, column=0, pady=10)
		clearFormBtn.grid(row=0, column=0, padx=10, pady=10)
		changePasswordBtn.grid(row=0, column=1, padx=10, pady=10)

	def changePassword(self):
		# Check if fields are empty
		if (isEmptyEntryWidgets(self.formEntryList)):
			self.formErrorMessage.configure(text="Some fields are empty!")
			return

		oldPassword = self.formEntryList[0].get()
		oldPasswordHash = hashlib.md5(oldPassword.encode("utf-8")).hexdigest()
		newPassword = self.formEntryList[1].get()
		confirmNewPassword = self.formEntryList[2].get()

		# Check if the new password is valid
		if not isValidPassword(newPassword):
			self.formErrorMessage.configure(text="Password can only be 6-20 characters with only numbers, letters, and symbols: !@#$%^&*(){}[]<>,+~-._")
			return
		
		# Check if passwords match
		if newPassword != confirmNewPassword:
			self.formErrorMessage.configure(text="Passwords must match!")
			return
		
		# User can only delete the account they're currently signed in to.
		# So query in the user's table for a matching username, and a matching password hash
		retrievedUser = self.master.session.query(User).filter_by(username=self.master.loggedInUser.username, passwordHash=oldPasswordHash).first() #type: ignore
		
		# If we didn't find a user with the current usernmae and password hash to current password, then they had to have gotten the password input wrong
		if not retrievedUser:
			self.formErrorMessage.configure(text="Old password entered is incorrect!")
			return
		
		# Save new password to user and commit it to the database
		retrievedUser.passwordHash = hashlib.md5(newPassword.encode("utf-8")).hexdigest()
		self.master.session.commit() #type: ignore
		self.master.session.close() #type: ignore

		# After a password is changed we log out our user
		self.master.logoutUser() #type: ignore
			

##### Delete Account Page #####
class deleteAccountPage(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		# Create edit form frame
		form = ctk.CTkFrame(self)
		form.pack(expand=True)
		# Create header of the form
		formHeader = ctk.CTkFrame(form, fg_color="transparent")
		formHeading = ctk.CTkLabel(formHeader, text="Delete Account", font=("Helvetica", 32))
		subHeading = ctk.CTkLabel(formHeader, text=f"Are you sure you want to delete '{self.master.loggedInUser.username}'?")
		self.formErrorMessage = ctk.CTkLabel(formHeader, text="")
		
		# Create the input section with form fields 
		formFieldsSection = ctk.CTkFrame(form)

		formFields = [
			{
				"text": "Username"
			},
			{
				"text": "Password", 
				"toggleHidden": True
			}
		]
		# Create list of form entries to get input later
		# Then create and position label and entry widgets for form
		self.formEntryList = []

		for x in range(len(formFields)):
			label = ctk.CTkLabel(formFieldsSection, text=formFields[x].get("text"))
			entry = ctk.CTkEntry(formFieldsSection)
			self.formEntryList.append(entry)
			label.grid(row=x, column=0, padx=10, pady=10)
			entry.grid(row=x, column=1, padx=10, pady=10)
			if (formFields[x].get("toggleHidden")):
				checkVar = ctk.StringVar(value="off")
				visibilityCheckBox = ctk.CTkCheckBox(formFieldsSection, variable=checkVar, command=lambda entry=entry, var=checkVar: toggleHidden(entry, var),  text="Hide", onvalue="on", offvalue="off")
				visibilityCheckBox.grid(row=x, column=2, padx=4, pady=10)

		formBtnsSection = ctk.CTkFrame(form, fg_color="transparent")
		clearFormBtn = ctk.CTkButton(formBtnsSection, text="Clear", command=lambda: clearEntryWidgets(self.formEntryList))
		deleteAccountBtn = ctk.CTkButton(formBtnsSection, text="Delete Account", command=self.deleteAccount)
		
		# Structure the remaining elements of the page
		formHeader.grid(row=0, column=0, padx=40, pady=10)
		formHeading.grid(row=0, column=0)
		subHeading.grid(row=1, column=0)
		self.formErrorMessage.grid(row=2, column=0)
		formFieldsSection.grid(row=1, column=0, pady=10)
		formBtnsSection.grid(row=2, column=0, pady=10)
		clearFormBtn.grid(row=0,column=0, padx=10, pady=10)
		deleteAccountBtn.grid(row=0,column=1, padx=10, pady=10)


	# Deletes the account/record of the currently logged in user from the database
	def deleteAccount(self):
		# Check if fields are empty
		if isEmptyEntryWidgets(self.formEntryList):
			self.formErrorMessage.configure(text="Some fields are empty!")
			return
		
		# Get input fields from forms
		username = self.formEntryList[0].get()
		password = self.formEntryList[1].get()
		passwordHash = hashlib.md5(password.encode("utf-8")).hexdigest()

		'''
		- Since user is deleting their own account, the username they enter should be the username of the currently logged in user.
		- As a result, for the form to be valid, the username and password must belong to the currently logged in user.		
		'''
		if self.master.loggedInUser.username == username and self.master.loggedInUser.passwordHash == passwordHash: #type: ignore
			# Delete the logged in user from the database and save those changes
			self.master.session.delete(self.master.loggedInUser) #type: ignore
			self.master.session.commit() #type: ignore
			# We can safely do the logout process on the user now, since their account does not exist anymore
			self.master.logoutUser() #type: ignore
		else:
			# Else, their username or password is wrong
			self.formErrorMessage.configure(text="Username or password is incorrect!")



			

###### The page for editting accounts #####
class editAccountPage(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master

		# Create edit form frame
		form = ctk.CTkFrame(self)
		form.pack(expand=True)

		# Create header of the form
		formHeader = ctk.CTkFrame(form, fg_color="transparent")
		formHeading = ctk.CTkLabel(formHeader, text="Edit Account", font=("Helvetica", 32))
		self.formErrorMessage = ctk.CTkLabel(formHeader, text="")
		
		# Create the input section with form fields 
		formFieldsSection = ctk.CTkFrame(form)
		formFields = [
			{
				"text": "Username",
				"value": self.master.loggedInUser.username,
			},
			{
				"text": "Email",
				"value": self.master.loggedInUser.email,
			},
			{
				"text": "First Name",
				"value": self.master.loggedInUser.firstName,
			},
			{
				"text": "Last Name",
				"value": self.master.loggedInUser.lastName,
			},
		]

		# Create list of form entries to get input later
		# Then create and position label and entry widgets for form
		self.formEntryList = []
		for x in range(len(formFields)):
			label = ctk.CTkLabel(formFieldsSection, text=formFields[x]["text"])
			entry = ctk.CTkEntry(formFieldsSection)
			
			# Insert the current value of a user's attribute into the entry widget to show the user 
			# their current account information
			entry.insert(0, formFields[x]["value"]) 

			# Structure the label and entry widget
			label.grid(row=x, column=0, pady=10, ipadx=10)
			entry.grid(row=x, column=1, pady=10, ipadx=10)
			self.formEntryList.append(entry)

		# Clear form button and then a confirm changes button
		formBtnsSection = ctk.CTkFrame(form, fg_color="transparent")
		clearFormBtn = ctk.CTkButton(formBtnsSection, text="Clear", command=lambda: clearEntryWidgets(self.formEntryList))
		confirmEditsBtn = ctk.CTkButton(formBtnsSection, text="Confirm Edits", command=self.editAccount)
		openChangePasswordBtn = ctk.CTkButton(formBtnsSection, text="Change Password", command=lambda: self.master.openPage("changePasswordPage")) #type: ignore
		openDeleteAccountBtn = ctk.CTkButton(formBtnsSection, text="Account Deletion", command=lambda: self.master.openPage("deleteAccountPage")) #type: ignore

		# Structure the remaining page elements accordingly
		formHeader.grid(row=0, column=0, padx=70, pady=10)
		formHeading.grid(row=0, column=0)
		self.formErrorMessage.grid(row=1, column=0)
		formFieldsSection.grid(row=1, column=0, pady=10, ipadx=10)
		formBtnsSection.grid(row=2, column=0, pady=10)
		confirmEditsBtn.grid(row=0, column=0, padx=10, pady=10)
		clearFormBtn.grid(row=1, column=0, padx=10, pady=10)
		openChangePasswordBtn.grid(row=2, column=0, padx=10, pady=10)
		openDeleteAccountBtn.grid(row=3, column=0, padx=10, pady=10)

	# Validates and edits the attributes (username, email, first name, and last name) of the currently logged in user
	def editAccount(self):
		# Check if fields are empty
		if (isEmptyEntryWidgets(self.formEntryList)):
			self.formErrorMessage.configure(text="Some fields are empty!")
			return
		
		# Get inputted values of the form
		username = self.formEntryList[0].get()
		email = self.formEntryList[1].get()
		firstName = self.formEntryList[2].get()
		lastName = self.formEntryList[3].get()

		# Validate the username
		if not isValidUsername(username):
			self.formErrorMessage.configure(text="Username is invalid!")
			return

		# Validate the email
		if not isValidEmail(email):
			self.formErrorMessage.configure(text="Email is invalid!")
			return
		
		'''
		- Check if email is already taken: Query for a user with the inputted username 
		- If the user exists, a user in the database was found with the inputted username
			Case 1: This could mean, a different user from the logged in user has the username
			Case 2: The currently logged in user kept their current username in the username entry field.
			So the retrievedUser is just a record of the currently logged in user. In this case, we want 
			to let the form go through. By putting "and self.master.loggedInUser != retrievedUser", we're making 
			sure that a different user from the currently logged in user already has the username that they entered.
			As a result, the user is able to submit the form when they don't change their username, and the system
			correctly detects when a separate user has their inputted username
		'''
		retrievedUser = self.master.session.query(User).filter_by(username=username).first() #type: ignore
		if retrievedUser and (self.master.loggedInUser != retrievedUser): #type: ignore
			self.formErrorMessage.configure(text="Username is already taken!")
			return
		
		# All form checks passed, so apply changes
		self.master.loggedInUser.username = username #type: ignore
		self.master.loggedInUser.email = email #type: ignore
		self.master.loggedInUser.firstName = firstName #type: ignore
		self.master.loggedInUser.lastName = lastName #type: ignore
		self.master.session.commit() #type: ignore

		# Then redirect user to the account page, so that they can see their changes
		self.master.openPage("userAccountPage") #type: ignore




##### The user account or profile page#####
class userAccountPage(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		# This extra frame just allows stuff to be centered onto the userAccountPage frame
		innerPageFrame = ctk.CTkFrame(self, fg_color="transparent")
		innerPageFrame.pack(expand=True)
		# Create section to store the user's profile picture
		userImageSection = tk.Canvas(innerPageFrame, highlightbackground="#eee", highlightthickness=1)
		
		avatarSourcePath = f"./assets/images/{self.master.loggedInUser.avatar}"
		image = Image.open(avatarSourcePath).resize((300, 300))
		imageWidget = ImageTk.PhotoImage(image=image)
		imageLabel = tk.Label(userImageSection, image=imageWidget)
		imageLabel.image = imageWidget #type: ignore
		imageLabel.grid(row=0, column=0)

		# Create section to store buttons on the user page
		userBtnsSection = ctk.CTkFrame(innerPageFrame, fg_color="transparent")
		openEditAvatarBtn = ctk.CTkButton(userBtnsSection, text="Edit Avatar", command=lambda: self.master.openPage("editAvatarPage")) #type: ignore
		openEditAccountBtn = ctk.CTkButton(userBtnsSection, text="Edit Account", command=lambda: self.master.openPage("editAccountPage")) #type: ignore
		confirmLogOutBtn = ctk.CTkButton(userBtnsSection, text="Log Out", command=self.master.logoutUser)
		openEditAvatarBtn.grid(row=0, column=0, pady=5)
		openEditAccountBtn.grid(row=1, column=0, pady=5)
		confirmLogOutBtn.grid(row=2, column=0, pady=5)

		# Create section to display user information
		# Get user information, and iteratively create labels to show that user information
		userInfoSection = ctk.CTkFrame(innerPageFrame, fg_color="transparent")
		userInfoFields = [
			{
				"text": "Username",
				"value": self.master.loggedInUser.username
			},
			{
				"text": "Email",
				"value": self.master.loggedInUser.email
			},
			{
				"text": "Name",
				"value": f"{self.master.loggedInUser.firstName} {self.master.loggedInUser.lastName}"
			}
		]
		for x in range(len(userInfoFields)):
			label = ctk.CTkLabel(userInfoSection, text=f"{userInfoFields[x].get('text')}: {userInfoFields[x].get('value')}", font=("Helvetica", 24))
			label.grid(row=x, column=0, sticky="W", pady=10)

		# Structure the 3 main sections of the user account page
		userImageSection.grid(row=0, column=0, padx=30, pady=10)
		userBtnsSection.grid(row=1, padx=30, column=0)
		userInfoSection.grid(row=0, column=1, padx=30)


##### User Registration Page ######
class userRegisterPage(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		
		# Create registration form frame
		form = ctk.CTkFrame(self)
		form.pack(expand=True)

		# Create form header and text elements for header
		formHeader = ctk.CTkFrame(form, fg_color="transparent")
		formHeading = ctk.CTkLabel(formHeader, text="Register", font=("Helvetica", 32))
		self.formErrorMessage = ctk.CTkLabel(formHeader, text="")

		# Create input section with form fields
		formFieldsSection = ctk.CTkFrame(form)
		formFields = [
			{
				"text": "Email",
			},
			{
				"text": "Username",
			},
			{
				"text": "First Name",
			},
			{
				"text": "Last Name",
			},
			{
				"text": "Password",
				"toggleHidden": True	
			},
			{
				"text": "Confirm Password",
				"toggleHidden": True
			},
		]		
		# Create list of form entries to get input later
		self.formEntryList = []
		# Iterate through object to create fields
		for x in range(len(formFields)):
			label = ctk.CTkLabel(formFieldsSection, text=formFields[x]["text"])
			entry = ctk.CTkEntry(formFieldsSection)
			self.formEntryList.append(entry)
			label.grid(row=x, column=0, padx=10, pady=10)
			entry.grid(row=x, column=1, padx=10, pady=10)
			# If there's a 'toggleHidden' attribute, add a checkbox
			# so that we can toggle visibility on the field
			if (formFields[x].get("toggleHidden")):
				checkVar = ctk.StringVar(value="off")
				visibilityCheckBox = ctk.CTkCheckBox(formFieldsSection, variable=checkVar, command=lambda entry=entry, var=checkVar: toggleHidden(entry, var),  text="Hide", onvalue="on", offvalue="off")
				visibilityCheckBox.grid(row=x, column=2, padx=4, pady=10)
			
		# Create section to have form buttons/actions
		formBtnsSection = ctk.CTkFrame(form, fg_color="transparent")
		openLoginBtn = ctk.CTkButton(formBtnsSection, text="Log into an existing account", command=lambda: self.master.openPage("userLoginPage")) #type: ignore
		confirmRegisterBtn = ctk.CTkButton(formBtnsSection, text="Confirm Registration", command=self.registerUser)
		clearFormBtn = ctk.CTkButton(formBtnsSection, text="Clear", command=lambda: clearEntryWidgets(self.formEntryList))

		# Structure the remaining elements of the page
		formHeader.grid(row=0, column=0, pady=10)
		formHeading.grid(row=0, column=0)
		self.formErrorMessage.grid(row=1, column=0)
		formFieldsSection.grid(row=1, column=0, pady=10, ipadx=10)
		formBtnsSection.grid(row=2, column=0, pady=10)
		clearFormBtn.grid(row=0, column=0, padx=10, pady=10)
		openLoginBtn.grid(row=0, column=1, padx=10, pady=10)
		confirmRegisterBtn.grid(row=0, column=2, padx=10, pady=10)

	# Registers a user in the database
	def registerUser(self):
		# Check if any fields are empty before moving on
		if isEmptyEntryWidgets(self.formEntryList):
			self.formErrorMessage.configure(text="Some fields are empty!")
			return

		# Get input field values
		email = self.formEntryList[0].get()
		username = self.formEntryList[1].get()
		firstName = self.formEntryList[2].get()
		lastName = self.formEntryList[3].get()
		password = self.formEntryList[4].get()
		confirmPassword = self.formEntryList[5].get()

		# Check if it's a valid email form
		if not isValidEmail(email):
			self.formErrorMessage.configure(text="Email isn't in valid form!")
			return
		
		# Check if username is valid
		if not isValidUsername(username):
			self.formErrorMessage.configure(text="Username length is 6-20 characters, and can only have numbers, letters, and underscores!")
			return
		
		# Check if password is valid
		if not isValidPassword(password):
			self.formErrorMessage.configure(text="Password can only be 6-20 characters with only numbers, letters, and symbols: !@#$%^&*(){}[]<>,+~-._")
			return
		
		# Check if password and the retryped password match
		if password != confirmPassword:
			self.formErrorMessage.configure(text="Passwords must match!")
			return
		
		
		# Check if there are any users with the inputted username
		retrievedUser = self.master.session.query(User).filter_by(username=username).first() #type: ignore
		if retrievedUser:
			self.formErrorMessage.configure(text="Usename already taken!")
			return
		
		# Create a new user based on the form information
		newUser = User(
			email=email,
			username=username,
			firstName=firstName,
			lastName=lastName,
			# For right now do a simple md5 hash, but later
			# we should use that api idea
			passwordHash=hashlib.md5(password.encode("utf-8")).hexdigest(),
			avatar="default_user.jpg"
		)

		# Add new user to the database
		self.master.session.add(newUser) #type: ignore
		self.master.session.commit() #type: ignore
		self.master.session.close() #type: ignore
		# Redirect user to login screen after they've successfully registered
		self.master.openPage("userLoginPage") #type: ignore



##### User login page #####
class userLoginPage(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		# Create login form frame
		form = ctk.CTkFrame(self)
		form.pack(expand=True)

		# Create header of the form
		formHeader = ctk.CTkFrame(form, fg_color="transparent")
		formHeading = ctk.CTkLabel(formHeader, text="Login", font=("Helvetica", 32))
		self.formErrorMessage = ctk.CTkLabel(formHeader, text="")
		
		# Create the input section with form fields 
		formFieldsSection = ctk.CTkFrame(form)

		formFields = [
			{
				"text": "Username"
			},
			{
				"text": "Password",
				"toggleHidden": True,
			}
		]
		# Create list of form entries to get input later
		self.formEntryList = []
		for x in range(len(formFields)):
			label = ctk.CTkLabel(formFieldsSection, text=formFields[x].get("text"))
			entry = ctk.CTkEntry(formFieldsSection)
			label.grid(row=x, column=0, pady=10, ipadx=10)
			entry.grid(row=x, column=1, pady=10, ipadx=10)
			if (formFields[x].get("toggleHidden")):
				checkVar = ctk.StringVar(value="off")
				visibilityCheckBox = ctk.CTkCheckBox(formFieldsSection, variable=checkVar, command=lambda entry=entry, var=checkVar: toggleHidden(entry, var),  text="Hide", onvalue="on", offvalue="off")
				visibilityCheckBox.grid(row=x, column=2, padx=4, pady=10)
			self.formEntryList.append(entry)

		# Create section to have form buttons/actions
		formBtnsSection = ctk.CTkFrame(form, fg_color="transparent")
		clearFormBtn = ctk.CTkButton(formBtnsSection, text="Clear", command=lambda: clearEntryWidgets(self.formEntryList))
		confirmLoginBtn = ctk.CTkButton(formBtnsSection, text="Confirm Login", command=self.loginUser)
		openRegisterAccountBtn = ctk.CTkButton(formBtnsSection, text="Register New Account", command=lambda: self.master.openPage("userRegisterPage")) #type: ignore
		
		# Structure the remaining elements of the page
		formHeader.grid(row=0, column=0, pady=10)
		formHeading.grid(row=0, column=0)
		self.formErrorMessage.grid(row=1, column=0)
		formFieldsSection.grid(row=1, column=0, pady=10, ipadx=10)
		formBtnsSection.grid(row=2, column=0, pady=10)
		clearFormBtn.grid(row=0, column=0, padx=10, pady=10)
		openRegisterAccountBtn.grid(row=0, column=1, padx=10, pady=10)
		confirmLoginBtn.grid(row=0, column=2, padx=10, pady=10)
		

	## Attempts to log in a user
	def loginUser(self):
		# Check if input fields are empty
		if (isEmptyEntryWidgets(self.formEntryList)):
			self.formErrorMessage.configure(text="Some fields are empty!")
			return
		
		# Get input values from the form
		username = self.formEntryList[0].get()
		password = self.formEntryList[1].get()
		passwordHash = hashlib.md5(password.encode("utf-8")).hexdigest()

		# Now check if the inputted username and password hash matches a record from the User table 
		retrievedUser = self.master.session.query(User).filter_by(username=username, passwordHash=passwordHash).first() #type: ignore
		if not retrievedUser:
			self.formErrorMessage.configure(text="Username or password is incorrect!")
			return
		
		# Assign the new logged in user
		self.master.loggedInUser = retrievedUser #type: ignore

		# Update the nav buttons now that the user is logged in
		# so that they actually work and aren't disabled
		self.master.header.updateNavButtons() #type: ignore

		# Redirect the user to the 'My Account' or the 'user account page'
		self.master.openPage("userAccountPage") #type: ignore



##### Application Header that has navbar #####
class Header(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master, fg_color="#f9a8d4", corner_radius=0)
		self.master = master
		
		# Create the navbar
		navbar = ctk.CTkFrame(self, fg_color="transparent")
		navbar.pack(expand=True)

		# Create header message 
		welcomeLabel = ctk.CTkLabel(navbar, text="Welcome to BookSmart.AI!", text_color="black", font=("Helvetica", 32))
		
		# Create frame for nav buttons
		navBtnFrame = ctk.CTkFrame(navbar, fg_color="transparent")
		self.navBtns = [] # List for all nav buttons
		self.navBtnMap = { # Create nav buttons with iteration
			"Home": "homePage",
			"AI Settings": "aiSettingsPage",
			"Library": "storyLibraryPage",
			"My Account": "userAccountPage",
		}
		colCount = 0
		for key in self.navBtnMap:
			navBtn = ctk.CTkButton(navBtnFrame, corner_radius=0, text=f"{key}", command=lambda k=key:self.master.openPage(self.navBtnMap[k])) #type: ignore
			navBtn.grid(row=0, column=colCount, padx=10)
			colCount += 1
			self.navBtns.append(navBtn)

		# Structure remaining elements
		welcomeLabel.grid(row=0, column=0)
		navBtnFrame.grid(row=1, column=0, pady=20)

		# Adjust nav button links depending on user login state
		self.updateNavButtons()
	'''
	- Update the nav buttons based on the login state of the user
	1. If user is logged in, nav buttons lead to their respective places
	2. Else: All nav buttons are disabled, preventing user from traversing to other pages until they log in
	'''
	def updateNavButtons(self):
		for button in self.navBtns:
			if (self.master.loggedInUser): #type: ignore
				button.configure(state="standard")
			else:
				button.configure(state="disabled")



###### Application Footer #####
class Footer(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master, fg_color="#f9a8d4", corner_radius=0)
		currentYear = datetime.datetime.now().year
		footerLabel = ctk.CTkLabel(self, text=f"BookSmart {currentYear}", text_color="black",	font=("Helvetica", 16))
		footerLabel.pack()



##### Main application #####
class App(ctk.CTk):
	def __init__(self):
		super().__init__()
		self.title("BookSmart.Ai")
		self.width = self.winfo_screenwidth()
		self.height = self.winfo_screenheight()
		self.geometry(f"{self.width}x{self.height}")

		# Attribute to keep track of the current page
		self.currentPage = None

		# If user is logged in, this will be a User class instance, representing 
		# the User that is currently logged into the application
		self.loggedInUser = None 

		# Frames in the application
		self.pageMap = {
			"userLoginPage": userLoginPage,
			"userRegisterPage": userRegisterPage,
			"userAccountPage": userAccountPage,
			"editAccountPage": editAccountPage,
			"deleteAccountPage": deleteAccountPage,
			"changePasswordPage": changePasswordPage,
			"storyLibraryPage": storyLibraryPage,
			"editAvatarPage": editAvatarPage,
			"aiSettingsPage": aiSettingsPage,
			"saveStoryPage": saveStoryPage,
			"homePage": homePage,
			"remixStoryPage": remixStoryPage,
			# Then add in our homePage as well
		}

		# Engine and session constructor that we're going to use 
		self.engine = create_engine("sqlite:///assets/PyProject.db")
		self.Session = sessionmaker(bind=self.engine)

		# The master session object we'll use throughout the application to interact with the database
		self.session = self.Session()

		# Array that keeps track of the messages in the most recent story or session
		# that the user created with the AI. Should be an array of Message Objects
		self.currentStoryMessages = []

		# Log into a user for dev purposes
		self.loggedInUser = self.session.query(User).filter_by(username="knguyen44").first()
		selectedStory = self.session.query(Story).filter_by(storyTitle="A really long title that's in the deep end. Of course!").first()


		# Call function to create navbar
		self.header = Header(self)
		self.header.pack(side="top", fill="x")
		footer = Footer(self)
		footer.pack(fill="x", side="bottom")

		self.openPage("saveStoryPage")
		
	def openPage(self, pageName, *args):
		try:
			pageClass = self.pageMap[pageName]
			if self.currentPage:
				self.currentPage.destroy()
			self.currentPage = pageClass(self, *args)
			self.currentPage.pack(fill="both", expand=True)
		except KeyError:
			print(f"Error: Page {pageName} doesn't exist")

	
	# Log the current user out of the application
	def logoutUser(self):
		# loggedInUser is none because the user is logging out 
		self.loggedInUser = None #type: ignore
		# Redirect the user to the login page
		self.openPage("userLoginPage") #type: ignore
		# Update nav buttons so that user can't access the pages associated with them
		self.header.updateNavButtons() #type: ignore



if __name__ == "__main__":
	app = App()
	app.mainloop()