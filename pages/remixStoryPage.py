import customtkinter as ctk
import sys
sys.path.append("..")
from classes.models import Message

'''
+ remixStoryPage: Frame that represents the page that allows the user to remix a story. User will be able 
	to input in a twist to the story that they have selected. Then after submission, the user is taken to the 
	AIChatPage to write their new story.

Attributes/Variables:
- story (Story): Story object that the user is remixing their story from. So this story is the inspiration for their
	remix.
- master: 'App' class instance from 'Main.py'
- form (CTkFrame): Frame that contains all form widgets
- formHeader (CTkFrame): Header of form
- formHeading (CTkLabel): Heading message for form
- subHeading (CTkLabel): a sub-heading that indicates what story the user is remixing off from
- formFieldsSection (CTkFrame): Contains all labels and input related widgets for the form
- remixLabel (CTkLabel): Label for remixInput
- remixInput (CTkTextBox): Textbox where the user enters their twist or remix on the selected story
- formBtnsSection (CTkFrame): Section that contains all of the buttons for the form
- clearRemixBtn (CTkButton): Button that clears the remixInput
- remixStoryBtn (CTkButton): Button that remixes the story and takes the user to the AIChatPage

Methods: 
- remixStory(self): Let's user remix a story and then redirects the user to the AIChatPage for it.
'''
class remixStoryPage(ctk.CTkFrame):
	def __init__(self, master):
		self.master = master
		super().__init__(self.master, fg_color=self.master.theme["main_clr"])
		self.story = self.master.remixStoryObj

		form = ctk.CTkFrame(self, fg_color=self.master.theme["sub_clr"])
		formHeader = ctk.CTkFrame(form, fg_color="transparent")
		formHeading = ctk.CTkLabel(formHeader, text="Remix A Story", font=("Helvetica", 32), text_color=self.master.theme["label_clr"])
		subHeading = ctk.CTkLabel(formHeader, text=f"Currently Remixing '{self.story.storyTitle}'!", wraplength=200, text_color=self.master.theme["label_clr"])

		self.formErrorMessage = ctk.CTkLabel(formHeader, text="", text_color=self.master.theme["label_clr"])

		formFieldsSection = ctk.CTkFrame(form, fg_color="transparent")
		remixLabel = ctk.CTkLabel(formFieldsSection, text="Enter your twist on this story!", wraplength=100, text_color=self.master.theme["label_clr"])
		self.remixInput = ctk.CTkTextbox(formFieldsSection, fg_color=self.master.theme["entry_clr"], text_color=self.master.theme["entry_text_clr"])

		formBtnsSection = ctk.CTkFrame(form, fg_color="transparent")
		clearRemixBtn = ctk.CTkButton(formBtnsSection, fg_color=self.master.theme["btn_clr"], hover_color=self.master.theme["hover_clr"],  text="Clear", command=lambda: self.remixInput.delete("0.0", "end"))
		remixStoryBtn = ctk.CTkButton(formBtnsSection, fg_color=self.master.theme["btn_clr"], hover_color=self.master.theme["hover_clr"],  text="Confirm Remix", command=self.remixStory)

		form.pack(expand=True)
		formHeader.grid(row=0, column=0, pady=10, padx=50)
		formHeading.grid(row=0, column=0)
		subHeading.grid(row=1, column=0)
		self.formErrorMessage.grid(row=2, column=0)
		formFieldsSection.grid(row=1, column=0, pady=10)
		remixLabel.grid(row=0, column=0, pady=10)
		self.remixInput.grid(row=1, column=0, pady=10)
		formBtnsSection.grid(row=2, column=0, pady=10)
		clearRemixBtn.grid(row=0, column=0, padx=10)
		remixStoryBtn.grid(row=0, column=1, padx=10)


	
	def remixStory(self):
		'''
		- Remixes a story using an existing story and user's input.
		1. userRemixMessage (Message): Message object representing the text that the user entered
		2. AIMessage (Message): Message object representing the text that the AI generated in reply
			to the user.
		'''
		# Check if user entered text for remixing
		if self.remixInput.get("1.0", "end-1c").strip() == "":
			self.formErrorMessage.configure(text="Please at least enter text for the remix!")
			return

		# If the user is remixing a story, they're choosing not to continue writing on a saved story 
		self.master.currentStory = self.story  

		# User is remixing a story, so change the booleans to indicate that the user
		# is currently remixing a story rather than continuing a saved one
		self.master.isSavedStory = False 
		self.master.isRemixedStory = True 

		# They are also starting a new chat, so we should remove all old unsaved story messages
		# Also clear AI of any past knowledge, they should only know about the inputted story and its twist
		self.master.unsavedStoryMessages = [] 
		self.master.storyGPT.clear() 

		# Concatenate that messages of the story into one string, that represents the content of the selected story
		storyText = ""
		for messageObj in self.story.messages:
			storyText += messageObj.text

		# Get AI's response, which will be our generator object, set it storyGenObj
		AIResponse = self.master.storyGPT.sendRemixPrompt(storyText, self.remixInput.get("1.0", "end-1c").strip()) 
		self.master.storyGenObj = AIResponse 

		# Redirect user to the ai chat page
		self.master.openPage("AIChatPage") 