import customtkinter as ctk
import sys
sys.path.append("..")
from classes.models import Story
from classes.utilities import isEmptyEntryWidgets, clearEntryWidgets

'''
+ saveStoryPage: Page where the user will save a a story. If we load the frame, that means the we're loading 
the form and the user is saving a completely new story. Else the class can be instantiated without being packed in so that 
the user makes updates to an existing story.

Attributes/Variables:
- form (CTkFrame): Container that contains all form widgets
- formHeader (CTkFrame): Header of the form
- formHeading (CTkLabel): Header message of the form
- storyStateMessage (CTkLabel): Label that indicates what kind of story they're saving
- formBtnsSection (CTkFrame): Frame that contains the form's buttons
- formErrorMessage (CTkLabel): Label that will show any form errors
- formFieldsSection (CTkFrame): Frame that holds form entry and label widgets
- storyTitleLabel (CTkLabel): Label for the storyTitleEntry
- storyTitleEntry (CTkEntry): Entry widget for entering in the saved story's title 
- clearFormBtn (CTkButton): Button that clears the form
- saveNewStoryBtn (CTkButton): Button that saves a new story
- updateSavedStoryBtn (CTkButton): Button that updates a saved story

Methods:
- updateExistingStory(self): Saves new changes to an existing saved story 
- saveNewStory(self): Saves a new story to the database
'''
class saveStoryPage(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master
		form = ctk.CTkFrame(self)	

		# Create and structure form widgets that are guaranteed to be on the page 
		formHeader = ctk.CTkFrame(form, fg_color="transparent")
		formHeading = ctk.CTkLabel(formHeader, text="Save Story", font=("Helvetica", 32))
		storyStateMessage = ctk.CTkLabel(formHeader, text="")
		formBtnsSection = ctk.CTkFrame(form, fg_color="transparent")
		form.pack(expand=True)
		formHeader.grid(row=0, column=0, pady=10, padx=80)
		formHeading.grid(row=0, column=0)
		storyStateMessage.grid(row=1, column=0)

		# If they're making changes to an existing story
		if self.master.isSavedStory: #type: ignore
			storyStateMessage.configure(text=f"Currently updating '{self.master.currentStory.storyTitle}'!")
			formBtnsSection.grid(row=1, column=0, pady=10)
			updateSavedStoryBtn = ctk.CTkButton(formBtnsSection, text="Update Story", command=self.updateExistingStory)
			updateSavedStoryBtn.grid(row=0, column=0)
		else:
		# Else the user is saving a new story to the database
			# If the new story they're saving is a remix
			if self.master.isRemixedStory:
				storyStateMessage.configure(text=f"Currently saving a new story remixed from {self.master.currentStory.storyTitle}!")
			else:
			# Else the new story they're saving isn't a remix
				storyStateMessage.configure(text="Currently saving a new story!")

			# Create widgets and structure them accrodingly
			self.formErrorMessage = ctk.CTkLabel(formHeader, text="")
			formFieldsSection = ctk.CTkFrame(form)		
			storyTitleLabel = ctk.CTkLabel(formFieldsSection, text="Story Title")
			self.storyTitleEntry = ctk.CTkEntry(formFieldsSection)
			clearFormBtn = ctk.CTkButton(formBtnsSection, text="Clear", command=lambda: clearEntryWidgets([self.storyTitleEntry]))
			saveNewStoryBtn = ctk.CTkButton(formBtnsSection, text="Save Story", command=self.saveNewStory)

			# Structure the widgets
			self.formErrorMessage.grid(row=2, column=0)
			formFieldsSection.grid(row=1, column=0, pady=10)
			storyTitleLabel.grid(row=0, column=0, pady=10, padx=10)
			self.storyTitleEntry.grid(row=0, column=1, pady=10, padx=10)
			formBtnsSection.grid(row=2, column=0, pady=10)
			clearFormBtn.grid(row=0, column=0, padx=10)
			saveNewStoryBtn.grid(row=0, column=1, padx=10)	

	'''
	- Updates or saves changes to an existing story and redirects user to the library page
	'''
	def updateExistingStory(self):
		# Put all of those unsaved messages into the saved story and save it to the database
		for unsavedMessage in self.master.unsavedStoryMessages: #type: ignore 
			self.master.currentStory.messages.append(unsavedMessage) #type: ignore
		self.master.session.commit() #type: ignore

		# Reset unsavedStoryMessages since all of the previous messages have been saved
		self.master.unsavedStoryMessages = [] #type: ignore
		
		# Redirect user to the story library page
		self.master.openPage("storyLibraryPage") #type: ignore
	

	'''
	- Saves a completely new story to the user's library; then redirects the user to the story library page
	'''
	def saveNewStory(self):
		# Check if fields are empty, put the entry widget in an array so that the function works
		if (isEmptyEntryWidgets([self.storyTitleEntry])):
			self.formErrorMessage.configure(text="Some fields are empty!")
			return

		# Create story object with the user's inputted title and the current messages
		newStory = Story(
			storyTitle=self.storyTitleEntry.get(),
			messages = self.master.unsavedStoryMessages, #type: ignore
		)

		# Reset unsavedStoryMessages since all of the previous messages have been saved
		self.master.unsavedStoryMessages = [] #type: ignore

		# Add the story to the current user and save the database
		self.master.loggedInUser.stories.append(newStory) #type: ignore
		self.master.session.commit() #type: ignore

		# Make the story that the user just saved to be the saved story that they're continuing
		self.master.currentStory = newStory #type: ignore

		# If the user was saving a remix, make sure the booleans indicate that the user is 
		# currently continuing a saved story.
		if self.master.isRemixedStory: #type: ignore
			self.master.isSavedStory = True #type: ignore
			self.master.isRemixedStory = False #type: ignore 

		# Redirect the user to the storyLibraryPage, which is where their new story should be
		self.master.openPage("storyLibraryPage") #type: ignore