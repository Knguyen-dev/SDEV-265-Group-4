import customtkinter as ctk
import sys
sys.path.append("..")
from classes.models import Message

class AIChatPage(ctk.CTkFrame):
	def __init__(self, master):
		super().__init__(master)
		self.master = master

		innerPageFrame = ctk.CTkFrame(self)
		innerPageFrame.pack(expand=True)

		header = ctk.CTkFrame(innerPageFrame, fg_color="transparent")
		heading = ctk.CTkLabel(header, text="Write Your Story!", font=("Helvetica", 32))
		
		# Message that shows the story of their story writing, whether they're writing a new story,
		# continuing an old one, or remixing a story, and other information
		storyStateMessage = ctk.CTkLabel(header, text="")

		# Message indicating status of the page, whether an error has occurred, or to show the user 
		# if they're still waiting on a message from the ai
		self.pageStatusMessage = ctk.CTkLabel(header, text="")
		
		# Text box that where all messages between user and ai will be shown
		self.chatBox = ctk.CTkTextbox(innerPageFrame, state="disabled", width=500, height=300)

		# Section with all of the input options the user has for the AIChatPage
		chatInputSection = ctk.CTkFrame(innerPageFrame, fg_color="transparent")
		self.chatEntry = ctk.CTkEntry(chatInputSection, width=300, placeholder_text="Send a message e.g. 'Once upon a time...'")
		self.openSaveStoryBtn = ctk.CTkButton(chatInputSection, text="Save Story", command=lambda: self.master.openPage("saveStoryPage")) #type: ignore
		self.sendChatBtn = ctk.CTkButton(chatInputSection, text="Send", command=self.sendUserChat)

		# Structure and style widgets accordingly
		header.grid(row=0, column=0, pady=10)
		heading.grid(row=0, column=0)
		storyStateMessage.grid(row=1, column=0)
		self.pageStatusMessage.grid(row=2, column=0)
		self.chatBox.grid(row=1, column=0, pady=10)
		chatInputSection.grid(row=2, column=0, pady=20)
		self.chatEntry.grid(row=0, column=0, padx=10)
		self.sendChatBtn.grid(row=0, column=1, padx=10)
		self.openSaveStoryBtn.grid(row=0, column=2, padx=10)

		# If the user is continuing a saved story, we should render the already saved messages from that story first
		if self.master.isSavedStory: #type: ignore
			for messageObj in self.master.currentStory.messages:
				self.renderChatMessage(messageObj)
			storyStateMessage.configure(text=f"Currently continuing '{self.master.currentStory.storyTitle}'!")
		elif self.master.isRemixedStory: #type: ignore
		# Else the user is currently writing a remix
			storyStateMessage.configure(text=f"Currently writing a remix based on {self.master.currentStory.storyTitle}!")
		else:
		# Else the user is writing a new story 
			storyStateMessage.configure(text=f"Currently continuing writing a new story!")

		# Then after, if there have been any messages that the user has made, but not saved, we render them
		if self.master.unsavedStoryMessages:
			for messageObj in self.master.unsavedStoryMessages:
				self.renderChatMessage(messageObj)
		

	# Accepts a Message object, and then renders it on the chat page
	def renderChatMessage(self, messageObj):
		# Configure the chatbox to normal so that text can be inserted
		self.chatBox.configure(state="normal")			

		# Logic for rendering a message
		# If it's an AI message
		if (messageObj.isAISender):
			# If the chatbox is empty, this is the first message, so render it properly with no extra space
			if self.chatBox.get("1.0", "end-1c") == "":
				self.chatBox.insert("1.0", f"StoryBot: {messageObj.text}")	
			else:
			# Else it's not the first message, so add extra spacing at the beginning of the message for aesthetic purposes
				self.chatBox.insert("end-1c", "\n\n" + f"StoryBot: {messageObj.text}") #type: ignore
		else:
		# Else it's a message from the user
			if self.chatBox.get("1.0", "end-1c") == "":
				self.chatBox.insert("1.0", f"{self.master.loggedInUser.username}: {messageObj.text}") #type: ignore
			else:
				self.chatBox.insert("end-1c", "\n\n" + f"{self.master.loggedInUser.username}: {messageObj.text}") #type: ignore

		# Scroll the chat window to the most recent message if needed
		self.chatBox.see("end-1c")

		# Set the chatbox to disabled now to prevent user from adding text to it
		self.chatBox.configure(state="disabled")
		
	
	'''
	- Sends the user chat message to the ai, for the ai to respond, then goes to render both of those chat messages
	1. Also saves chat messages for managing the 'history' of the messages in the current story
	'''
	def sendUserChat(self):
		# Get the user's message as an object
		userMessage = Message(text=self.chatEntry.get(), isAISender=False)

		# Then clear user's chat entry since they sent the message, we don't want to force them to clear it themselves
		self.chatEntry.delete(0, "end")

		# Call function to get the AI's response message 
		AIMessage = Message(text="Sample AI Response", isAISender=True)

		# Add those messages sequentially in the unsavedStoryMessages array so that 
		# we can keep track of the user's messages
		self.master.unsavedStoryMessages.append(userMessage) #type: ignore
		self.master.unsavedStoryMessages.append(AIMessage) #type: ignore
		
		# Render the user's messages sequentially, so the user message is always rendered before the ai message
		self.renderChatMessage(userMessage)
		self.renderChatMessage(AIMessage)