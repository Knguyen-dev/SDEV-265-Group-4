import customtkinter as ctk
import sys
sys.path.append("..")
from classes.models import Story
from classes.utilities import isEmptyEntryWidgets, clearEntryWidgets

'''
+ saveStoryPage: Page where the user will save a a story. If we load the frame, that means the we're loading 
the form and the user is saving a completely new story. Else the class can be instantiated without being packed in so that 
the user makes updates to an existing story.
'''
class saveStoryPage(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master

		# user is trying to save a completely new story, so we'll give them a form
		form = ctk.CTkFrame(self)		
		formHeader = ctk.CTkFrame(form, fg_color="transparent")
		formHeading = ctk.CTkLabel(formHeader, text="Save Story", font=("Helvetica", 32))
		storyStateMessage = ctk.CTkLabel(formHeader, text="")
		formBtnsSection = ctk.CTkFrame(form, fg_color="transparent")

		# Create necessary widgets regardless of whether the user is updating an existing story or saving a new one
		form.pack(expand=True)
		formHeader.grid(row=0, column=0, pady=10, padx=80)
		formHeading.grid(row=0, column=0)
		storyStateMessage.grid(row=1, column=0)

		# Depending on whether the user is saving changes to an existing story or saving a completely new story, 
		# our page will form differently 

		# If they're making changes to an existing story
		if self.master.isSavedStory: #type: ignore
			storyStateMessage.configure(text=f"Currently updating '{self.master.currentStory.storyTitle}'!")
			formBtnsSection.grid(row=1, column=0, pady=10)
			updateSavedStoryBtn = ctk.CTkButton(formBtnsSection, text="Update Story", command=self.updateExistingStory)
			updateSavedStoryBtn.grid(row=0, column=0)
		else:	
		# Depending on whether saving a remix or a completely new story change change the label text
			# If the user is saving a remix
			if self.master.isRemixedStory:
				storyStateMessage.configure(text=f"Currently saving a new story remixed from {self.master.currentStory.storyTitle}!")
			else:
			# Else the user is saving a completely new story 
				storyStateMessage.configure(text="Currently saving a new story!")

			# Create widgets and structure them accrodingly
			self.formErrorMessage = ctk.CTkLabel(formHeader, text="")
			formFieldsSection = ctk.CTkFrame(form)		
			label = ctk.CTkLabel(formFieldsSection, text="Story Title")
			self.storyTitleEntry = ctk.CTkEntry(formFieldsSection)
			clearFormBtn = ctk.CTkButton(formBtnsSection, text="Clear", command=lambda: clearEntryWidgets([self.storyTitleEntry]))
			saveNewStoryBtn = ctk.CTkButton(formBtnsSection, text="Save Story", command=self.saveNewStory)

			self.formErrorMessage.grid(row=2, column=0)
			formFieldsSection.grid(row=1, column=0, pady=10)
			label.grid(row=0, column=0, pady=10, padx=10)
			self.storyTitleEntry.grid(row=0, column=1, pady=10, padx=10)
			formBtnsSection.grid(row=2, column=0, pady=10)
			clearFormBtn.grid(row=0, column=0, padx=10)
			saveNewStoryBtn.grid(row=0, column=1, padx=10)	

				
	# Updates or saves changes to an existing story and redirects user to the library page
	def updateExistingStory(self):
		# Put all of those unsaved messages into the saved story 
		for unsavedMessage in self.master.unsavedStoryMessages: #type: ignore 
			self.master.currentStory.messages.append(unsavedMessage) #type: ignore

		# Reset unsavedStoryMessages since all of the previous messages have been saved
		self.master.unsavedStoryMessages = [] #type: ignore

		# Update the story's messages in the database
		self.master.session.commit() #type: ignore

		# Redirect user to the story library page
		self.master.openPage("storyLibraryPage") #type: ignore
	

	
	# Saves a completely new story to the user's library; then redirects the user to the story library page
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

		# The story that the user just saved is now the saved story that they're continuing
		self.master.currentStory = newStory #type: ignore

		# If the story the user was saving was a remix, we reset it
		# As a result, the new story becomes the saved story that the user is continuing
		if self.master.isRemixedStory: #type: ignore
			self.master.isSavedStory = True #type: ignore
			self.master.isRemixedStory = False #type: ignore 

		# Redirect the user to the storyLibraryPage, which is where their new story should be
		self.master.openPage("storyLibraryPage") #type: ignore