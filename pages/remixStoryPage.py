import customtkinter as ctk
import sys
sys.path.append("..")
from classes.models import Message

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
	+ remixStory: Remixes a story using an existing story and user's input. This should start a new chat as the 
	user is now writing a new story that they haven't saved yet. If they save the remix, we treat it as the user is saving a completely new 
	story. As a result we save their remix as a new story, whilst keeping the story they remixed off of (the inspiration) unchanged.
	'''
	def remixStory(self):
		# If the user is remixing a story, they're choosing not to continue writing on a saved story 
		self.master.currentStory = self.story #type: ignore 

		# User is remixing a story, so change the booleans to indicate that the user
		# is currently remixing a story rather than continuing a saved one
		self.master.isSavedStory = False #type: ignore
		self.master.isRemixedStory = True #type: ignore

		# They are also starting a new chat, so we should remove all old unsaved story messages
		self.master.unsavedStoryMessages = [] #type: ignore

		# Get the text of the remix
		userRemixMessage = Message(text=self.remixInput.get("1.0", "end-1c"), isAISender=False)
	
		# At this point we'd send the ai the text of the story being remixed
		AIMessage = Message(text="Sample AI Remix Message", isAISender=True)

		# Put both of those messages into unsaved message 
		self.master.unsavedStoryMessages.append(userRemixMessage) #type: ignore
		self.master.unsavedStoryMessages.append(AIMessage) #type: ignore

		# Redirect user to the ai chat page
		self.master.openPage("AIChatPage") #type: ignore